# cascade

High-performance Discord user API wrapper for Python.

## Install

```bash
pip install cascade-discord
```

Voice support:
```bash
pip install cascade-discord[voice]
```

## Quick Start

```python
from cascade import Session

session = Session('your_token')

@session.event
async def on_ready():
    print(f'{session.user.name} ready')

@session.event
async def on_message(message):
    if message.content == '!ping':
        await message.reply('pong')

session.run()
```

## Features

- Full Gateway v10 with reconnect and resume
- 120+ REST endpoints
- Rate limit handling with per-bucket tracking
- Platform spoofing (desktop, mobile, web, console, VR)
- Rich presence builder
- Voice support (FFmpeg + Opus)
- Interactions (buttons, select menus, modals)
- AutoMod rules
- Layered caching (LRU/LFU/FIFO/TTL)
- Token protection and fingerprint randomization
- Commands framework
- Quest system with safe heartbeat loops
- Thread and webhook management
- Bulk operations

## Examples

### Send Messages

```python
channel = session.get_channel(channel_id)
await channel.send('hello')

user = session.get_user(user_id)
await user.send('dm')
```

### Friend Requests

```python
await session.send_friend_request('username')

friends = await session.fetch_friends()
for friend in friends:
    print(friend.display_name)
```

### Join Servers

```python
await session.accept_invite('discord-api')
```

**Note**: Some servers require captcha verification. You'll get a 400 error with captcha details — handle this in your application.

### Quests

```python
quests = await session.quests.get_quests()
active = await session.quests.get_active_quests()

for quest in active:
    await session.quests.run_heartbeat_loop(quest.id)
```

### Rich Presence

```python
from cascade import Activity

activity = Activity.playing('My Game')
await session.change_presence(status='online', activity=activity)
```

### Threads

```python
thread = await channel.create_thread('Thread Name')
await thread.join()
await thread.send('first message')
```

### Webhooks

```python
webhook = await session.rest.get_webhook(webhook_id)
await webhook.send('webhook message')
```

### Bulk Operations

```python
messages = await channel.fetch_messages(limit=100)
message_ids = [m.id for m in messages]
await channel.bulk_delete(message_ids)
```

## Documentation

[https://cascade-discord.readthedocs.io](https://cascade-discord.readthedocs.io)

## Links

- **GitHub**: [https://github.com/kinyewest/cascade-rework](https://github.com/kinyewest/cascade-rework)
- **PyPI**: [https://pypi.org/project/cascade-discord](https://pypi.org/project/cascade-discord)
- **Docs**: [https://cascade-discord.readthedocs.io](https://cascade-discord.readthedocs.io)

## License

MIT
