from urllib.parse import quote
from typing import Any

BASE = 'https://discord.com/api/v10'


def _escape(val: Any) -> str:
    return quote(str(val).strip(), safe='')


def channel(channel_id: Any) -> str:
    return f'{BASE}/channels/{_escape(channel_id)}'


def channel_messages(channel_id: Any) -> str:
    return f'{BASE}/channels/{_escape(channel_id)}/messages'


def channel_message(channel_id: Any, message_id: Any) -> str:
    return f'{BASE}/channels/{_escape(channel_id)}/messages/{_escape(message_id)}'


def channel_typing(channel_id: Any) -> str:
    return f'{BASE}/channels/{_escape(channel_id)}/typing'


def channel_pins(channel_id: Any) -> str:
    return f'{BASE}/channels/{_escape(channel_id)}/pins'


def channel_pin(channel_id: Any, message_id: Any) -> str:
    return f'{BASE}/channels/{_escape(channel_id)}/pins/{_escape(message_id)}'


def guild(guild_id: Any) -> str:
    return f'{BASE}/guilds/{_escape(guild_id)}'


def guild_channels(guild_id: Any) -> str:
    return f'{BASE}/guilds/{_escape(guild_id)}/channels'


def guild_members(guild_id: Any) -> str:
    return f'{BASE}/guilds/{_escape(guild_id)}/members'


def guild_member(guild_id: Any, user_id: Any) -> str:
    return f'{BASE}/guilds/{_escape(guild_id)}/members/{_escape(user_id)}'


def guild_bans(guild_id: Any) -> str:
    return f'{BASE}/guilds/{_escape(guild_id)}/bans'


def guild_ban(guild_id: Any, user_id: Any) -> str:
    return f'{BASE}/guilds/{_escape(guild_id)}/bans/{_escape(user_id)}'


def guild_roles(guild_id: Any) -> str:
    return f'{BASE}/guilds/{_escape(guild_id)}/roles'


def guild_role(guild_id: Any, role_id: Any) -> str:
    return f'{BASE}/guilds/{_escape(guild_id)}/roles/{_escape(role_id)}'


def user(user_id: Any) -> str:
    return f'{BASE}/users/{_escape(user_id)}'


def me() -> str:
    return f'{BASE}/users/@me'


def me_guilds() -> str:
    return f'{BASE}/users/@me/guilds'


def me_guild(guild_id: Any) -> str:
    return f'{BASE}/users/@me/guilds/{_escape(guild_id)}'


def me_channels() -> str:
    return f'{BASE}/users/@me/channels'


def me_connections() -> str:
    return f'{BASE}/users/@me/connections'


def me_settings() -> str:
    return f'{BASE}/users/@me/settings'


def gateway() -> str:
    return f'{BASE}/gateway'


def gateway_bot() -> str:
    return f'{BASE}/gateway/bot'


def relationships() -> str:
    return f'{BASE}/users/@me/relationships'


def relationship(user_id: Any) -> str:
    return f'{BASE}/users/@me/relationships/{_escape(user_id)}'


def applications() -> str:
    return f'{BASE}/applications'


def application(app_id: Any) -> str:
    return f'{BASE}/applications/{_escape(app_id)}'
