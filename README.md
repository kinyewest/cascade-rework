# cascade-rework

High-performance, hardened Discord user API client and automation framework for Python.

Built with an emphasis on connection reliability, realistic protocol simulation, and security hardening.

---

## Installation

Install directly from the repository:

```bash
pip install git+https://github.com/kinyewest/cascade-rework.git
```

### Optional Dependencies

- **Voice Support** (PyNaCl + opuslib):
  ```bash
  pip install "git+https://github.com/kinyewest/cascade-rework.git#egg=cascade-discord[voice]"
  ```
- **Token Protection & Cryptography**:
  ```bash
  pip install "git+https://github.com/kinyewest/cascade-rework.git#egg=cascade-discord[security]"
  ```

---

## Quick Start

### Basic Session

```python
import os
from cascade import Session

# Load token securely from environment variable
session = Session.from_env("DISCORD_TOKEN")

@session.event
async def on_ready():
    print(f"Logged in as {session.user.name}")

@session.event
async def on_message(message):
    if message.content == "!ping":
        await message.reply("pong")

session.run()
```

### Selfbot Commands Framework

```python
from cascade.ext.commands import Bot, check
from cascade.utils.checks import is_owner

# Selfbot mode is enabled by default (commands only execute for your account)
bot = Bot.from_env("DISCORD_TOKEN", command_prefix=".")

@bot.command()
async def ping(ctx):
    await ctx.reply("pong!")

@bot.command()
@check(is_owner())
async def status(ctx, *, text: str):
    await ctx.reply(f"Status updated: {text}")

bot.run()
```

---

## Security & Protocol Hardening

`cascade-rework` includes built-in safeguards to protect user credentials and mimic authentic Discord client behavior:

- **Token Masking in Representations**: `Session`, `Bot`, `RestClient`, and `GatewayShard` mask user tokens in `__repr__` (e.g., `token='MTIz...YYYY'`), preventing credentials from leaking into terminal output, error logs, or stack traces.
- **Strict Host Verification**: `RestClient` rejects requests to external, third-party domains, preventing authenticated Discord tokens from accidentally being dispatched to untrusted endpoints.
- **Path Traversal Sanitization**: All REST identifiers, invite codes, and parameters are URL-quoted to protect against path traversal and unintended endpoint execution.
- **Accurate Platform Spoofing**: `PlatformSpoofer` configures consistent client fingerprints across Desktop, Mobile (Android / iOS), macOS, and Linux, ensuring client-hint headers (`Sec-Ch-Ua*`) match the spoofed platform.
- **Clean Gateway Identify**: Gateway connections adhere strictly to user client capabilities without sending bot-specific intents.
- **Non-Recursive Event Waiters**: `EventDispatcher.wait_for` uses an iterative waiter queue to avoid `RecursionError` and handle timeouts accurately under heavy server activity.
- **FFmpeg Whitelist**: Audio subprocess execution strictly whitelists safe protocols (`file,http,https,tcp,tls,crypto`) and validates local file targets before execution.

---

## Examples

### Platform Spoofing

Simulate different devices and clients seamlessly:

```python
from cascade import Session

# Options: "desktop", "windows", "macos", "linux", "android", "ios", "web"
session = Session.from_env("DISCORD_TOKEN", platform="android")
```

### Adaptive Rate Limiting

```python
from cascade import Session

session = Session.from_env("DISCORD_TOKEN", smart_ratelimit=True)
```

### Sending Messages & DM

```python
channel = session.get_channel(channel_id)
await channel.send("Hello from cascade!")

user = session.get_user(user_id)
await user.send("Private message")
```

### Server Invites & Captcha Handling

```python
import cascade

try:
    await session.accept_invite("invite-code")
    print("Joined server!")
except cascade.CaptchaRequired as e:
    print(f"Captcha required: {e.captcha_service} (Sitekey: {e.captcha_sitekey})")
```

### Rich Presence

```python
from cascade import Activity

activity = Activity.playing("Playing a game")
await session.change_presence(status="online", activity=activity)
```

---

## Links

- **GitHub Repository**: [https://github.com/kinyewest/cascade-rework](https://github.com/kinyewest/cascade-rework)
- **Documentation**: [https://cascade-discord.readthedocs.io](https://cascade-discord.readthedocs.io)

---

## License

Released under the [MIT License](LICENSE).
