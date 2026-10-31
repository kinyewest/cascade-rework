from typing import Optional, Dict, Any, TYPE_CHECKING
from dataclasses import dataclass
from ..types.enums import WebhookType

if TYPE_CHECKING:
    from ..core.session import Session

@dataclass
class Webhook:
    id: int
    type: WebhookType
    guild_id: Optional[int]
    channel_id: int
    name: Optional[str]
    avatar: Optional[str]
    token: Optional[str] = None
    application_id: Optional[int] = None
    user_id: Optional[int] = None
    source_guild_id: Optional[int] = None
    source_channel_id: Optional[int] = None
    url: Optional[str] = None
    _session: Optional['Session'] = None
    
    @classmethod
    def from_dict(cls, data: dict, session: 'Session' = None) -> 'Webhook':
        return cls(
            id=int(data['id']),
            type=WebhookType(data['type']),
            guild_id=int(data['guild_id']) if data.get('guild_id') else None,
            channel_id=int(data['channel_id']),
            name=data.get('name'),
            avatar=data.get('avatar'),
            token=data.get('token'),
            application_id=int(data['application_id']) if data.get('application_id') else None,
            user_id=int(data['user']['id']) if data.get('user') else None,
            source_guild_id=int(data['source_guild']['id']) if data.get('source_guild') else None,
            source_channel_id=int(data['source_channel']['id']) if data.get('source_channel') else None,
            url=data.get('url'),
            _session=session
        )
    
    @property
    def avatar_url(self) -> Optional[str]:
        if self.avatar:
            return f'https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png'
        return None
    
    @property
    def default_avatar_url(self) -> str:
        return f'https://cdn.discordapp.com/embed/avatars/{int(self.id) % 5}.png'

    async def send(self, content: str = None, **kwargs) -> Dict[str, Any]:
        if not self.token:
            raise ValueError('Webhook token is required to execute webhook')
        payload = {}
        if content:
            payload['content'] = content
        payload.update(kwargs)
        return await self._session.rest.execute_webhook(str(self.id), self.token, **payload)

    async def edit_message(self, message_id: int, **kwargs) -> Dict[str, Any]:
        if not self.token:
            raise ValueError('Webhook token is required')
        return await self._session.rest.edit_webhook_message(str(self.id), self.token, str(message_id), **kwargs)

    async def delete_message(self, message_id: int) -> None:
        if not self.token:
            raise ValueError('Webhook token is required')
        await self._session.rest.delete_webhook_message(str(self.id), self.token, str(message_id))

    async def fetch_message(self, message_id: int) -> Dict[str, Any]:
        if not self.token:
            raise ValueError('Webhook token is required')
        return await self._session.rest.get_webhook_message(str(self.id), self.token, str(message_id))
