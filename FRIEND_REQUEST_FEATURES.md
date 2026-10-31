# Friend Request Features in Cascade

**Yes! Cascade has full friend request support.**

## Features Available:

### 1. Send Friend Requests
```python
await session.send_friend_request('username#0')
```

### 2. Fetch All Relationships
```python
relationships = await session.fetch_relationships()
for rel in relationships:
    if rel.is_friend:
        print(f'Friend: {rel.display_name}')
    elif rel.is_incoming_request:
        print(f'Incoming request from: {rel.display_name}')
    elif rel.is_outgoing_request:
        print(f'Outgoing request to: {rel.display_name}')
    elif rel.is_blocked:
        print(f'Blocked: {rel.display_name}')
```

### 3. Fetch Only Friends
```python
friends = await session.fetch_friends()
for friend in friends:
    print(f'{friend.display_name} (since {friend.since})')
```

### 4. Fetch Only Blocked Users
```python
blocked = await session.fetch_blocked()
for user in blocked:
    print(f'Blocked: {user.display_name}')
```

### 5. Accept Incoming Friend Requests
```python
relationships = await session.fetch_relationships()
for rel in relationships:
    if rel.is_incoming_request:
        await rel.accept()
        print(f'Accepted friend request from {rel.display_name}')
```

### 6. Remove Friends or Cancel Requests
```python
await relationship.remove()
```

### 7. Block Users
```python
await relationship.block()
```

### 8. Set Nicknames for Friends
```python
await relationship.set_nickname('My Best Friend')
```

### 9. Open DM with Friend
```python
dm_channel = await relationship.open_dm()
```

### 10. Gateway Events for Friend Requests
```python
@session.event
async def on_relationship_add(relationship):
    if relationship.is_incoming_request:
        print(f'New friend request from {relationship.display_name}!')
        await relationship.accept()

@session.event
async def on_relationship_remove(relationship):
    print(f'Relationship ended with {relationship.display_name}')
```

## Complete Example:

```python
from cascade import Session

session = Session('YOUR_TOKEN')

@session.event
async def on_ready():
    print(f'Logged in as {session.user.name}')
    
    print('\n=== Your Friends ===')
    friends = await session.fetch_friends()
    for friend in friends:
        print(f'- {friend.display_name}')
    
    print('\n=== Incoming Friend Requests ===')
    relationships = await session.fetch_relationships()
    incoming = [r for r in relationships if r.is_incoming_request]
    
    for req in incoming:
        print(f'Request from: {req.display_name}')
        choice = input('Accept? (y/n): ')
        if choice.lower() == 'y':
            await req.accept()
            print(f'Accepted!')
    
    print('\n=== Send Friend Request ===')
    username = input('Enter username: ')
    try:
        await session.send_friend_request(username)
        print(f'Sent friend request to {username}')
    except Exception as e:
        print(f'Failed: {e}')

@session.event
async def on_relationship_add(relationship):
    if relationship.is_incoming_request:
        print(f'\n🔔 New friend request from {relationship.display_name}!')

session.run()
```

## Relationship Types:

- `FRIEND = 1` — Mutual friend
- `BLOCKED = 2` — Blocked user
- `INCOMING_REQUEST = 3` — They sent you a request
- `OUTGOING_REQUEST = 4` — You sent them a request
- `IMPLICIT = 5` — Implicit relationship (e.g., in same DM group)

## Properties:

- `relationship.user_id` — User ID
- `relationship.username` — Username
- `relationship.global_name` — Display name
- `relationship.display_name` — Nickname > global_name > username
- `relationship.nickname` — Your private nickname for them
- `relationship.avatar_url` — Avatar CDN URL
- `relationship.since` — ISO timestamp when relationship created
- `relationship.is_friend` — Boolean
- `relationship.is_blocked` — Boolean
- `relationship.is_incoming_request` — Boolean
- `relationship.is_outgoing_request` — Boolean

## Methods:

- `await relationship.accept()` — Accept incoming friend request
- `await relationship.remove()` — Remove friend / cancel request
- `await relationship.block()` — Block user
- `await relationship.set_nickname('name')` — Set private nickname
- `await relationship.open_dm()` — Create/get DM channel

---

**TL;DR: Yes, cascade has friend requests! Use `session.send_friend_request()`, `session.fetch_relationships()`, and the `Relationship` entity with `.accept()`, `.remove()`, `.block()` methods.**
