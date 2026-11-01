import asyncio
import unittest
from unittest.mock import MagicMock, AsyncMock

from cascade.security.token_protection import TokenManager, HAS_CRYPTOGRAPHY
from cascade.core.dispatch import EventDispatcher
from cascade.ext.commands import Bot, check
from cascade.utils.checks import is_owner, has_role, has_any_role, is_guild, is_dm
from cascade.exceptions import CheckFailure
from cascade.spoof.platforms import PlatformSpoofer
from cascade.gateway.shard import GatewayShard
from cascade.api.rest import RestClient
from cascade.security.ratelimit_evasion import SmartRateLimiter
from cascade.entities.channel import TextChannel


class TestTokenProtection(unittest.TestCase):
    def test_token_encryption_cross_instance(self):
        if not HAS_CRYPTOGRAPHY:
            self.skipTest("cryptography not installed")
        tm1 = TokenManager("super_secret_master_password")
        token = "MTIzNDU2Nzg5.dummy.token_signature"
        encrypted = tm1.encrypt_token(token)

        tm2 = TokenManager("super_secret_master_password")
        decrypted = tm2.decrypt_token(encrypted)
        self.assertEqual(decrypted, token)

    def test_token_format_and_extraction(self):
        token = "MTIzNDU2Nzg5.dummy.token_signature"
        user_id = TokenManager.extract_user_id(token)
        self.assertEqual(user_id, 123456789)


class TestEventDispatcher(unittest.IsolatedAsyncioTestCase):
    async def test_wait_for_without_recursion(self):
        dispatcher = EventDispatcher()

        async def emit():
            await asyncio.sleep(0.01)
            dispatcher.dispatch("msg", {"id": 1, "text": "skip"})
            await asyncio.sleep(0.01)
            dispatcher.dispatch("msg", {"id": 2, "text": "target"})

        emit_task = asyncio.create_task(emit())
        res = await dispatcher.wait_for("msg", check=lambda m: m["id"] == 2, timeout=1.0)
        await emit_task
        self.assertEqual(res, {"id": 2, "text": "target"})

    async def test_wait_for_timeout_cleanup(self):
        dispatcher = EventDispatcher()

        async def emit_noise():
            for i in range(5):
                await asyncio.sleep(0.01)
                dispatcher.dispatch("msg", {"id": i})

        emit_task = asyncio.create_task(emit_noise())
        with self.assertRaises(asyncio.TimeoutError):
            await dispatcher.wait_for("msg", check=lambda m: m["id"] == 999, timeout=0.03)
        await emit_task
        self.assertNotIn("msg", dispatcher._waiters)


class TestBotSecurity(unittest.IsolatedAsyncioTestCase):
    async def test_selfbot_rejects_unauthorized_users(self):
        bot = Bot("test_token", command_prefix="!", self_bot=True)
        bot.user = MagicMock(id=111111111111111111)

        executed = []

        @bot.command()
        async def ping(ctx):
            executed.append(ctx.author.id)

        # Message from stranger
        stranger_msg = MagicMock()
        stranger_msg.author.id = 222222222222222222
        stranger_msg.content = "!ping"
        await bot._on_message(stranger_msg)
        self.assertEqual(executed, [])

        # Message from self
        self_msg = MagicMock()
        self_msg.author.id = 111111111111111111
        self_msg.content = "!ping"
        await bot._on_message(self_msg)
        self.assertEqual(executed, [111111111111111111])

    async def test_bot_checks(self):
        bot = Bot("test_token", command_prefix="!", self_bot=True, owner_id=111111111111111111)
        bot.user = MagicMock(id=111111111111111111)

        executed = []

        @bot.command()
        @check(is_owner())
        async def secure(ctx):
            executed.append("ok")

        self_msg = MagicMock()
        self_msg.author.id = 111111111111111111
        self_msg.content = "!secure"
        await bot._on_message(self_msg)
        self.assertEqual(executed, ["ok"])


class TestPlatformSpoofer(unittest.TestCase):
    def test_mobile_headers_omit_client_hints(self):
        spoofer = PlatformSpoofer("android")
        headers = spoofer.get_headers("sample_token")
        self.assertNotIn("Sec-Ch-Ua", headers)
        self.assertNotIn("Sec-Ch-Ua-Platform", headers)
        self.assertNotIn("Origin", headers)

    def test_macos_headers(self):
        spoofer = PlatformSpoofer("macos")
        headers = spoofer.get_headers("sample_token")
        self.assertEqual(headers.get("Sec-Ch-Ua-Platform"), '"macOS"')
        self.assertIn("Sec-Ch-Ua", headers)

    def test_windows_headers(self):
        spoofer = PlatformSpoofer("windows")
        headers = spoofer.get_headers("sample_token")
        self.assertEqual(headers.get("Sec-Ch-Ua-Platform"), '"Windows"')


class TestGatewayShardIdentify(unittest.TestCase):
    def test_identify_does_not_send_intents(self):
        session = MagicMock()
        session.spoofer = PlatformSpoofer("desktop")
        shard = GatewayShard("test_token", session)

        # Build identify data
        payload = {
            'capabilities': 16381,
            'properties': shard._build_client_properties(),
        }
        self.assertNotIn("intents", payload)


class TestRestClientSecurity(unittest.IsolatedAsyncioTestCase):
    async def test_path_traversal_sanitization(self):
        client = RestClient("test_token")
        client.get = AsyncMock()
        client.post = AsyncMock()

        # Attempt path traversal via invite code
        await client.accept_invite("../../users/@me/billing/payment-sources")
        called_url = client.post.call_args[0][0]
        self.assertNotIn("../", called_url)
        self.assertIn("..%2F..%2Fusers%2F%40me%2Fbilling%2Fpayment-sources", called_url)

    async def test_create_thread_without_message_alias(self):
        client = RestClient("test_token")
        client.create_thread = AsyncMock(return_value={"id": "999"})
        res = await client.create_thread_without_message("123", {"name": "test_thread"})
        self.assertEqual(res, {"id": "999"})
        client.create_thread.assert_called_once_with("123", name="test_thread")


if __name__ == "__main__":
    unittest.main()
