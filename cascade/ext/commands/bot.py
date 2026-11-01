import asyncio
from typing import Callable, Dict, Optional, Union, Set, List
from ...core.session import Session
from ...exceptions import CheckFailure
from .context import Context


class Bot(Session):
    def __init__(
        self,
        token: str,
        *,
        command_prefix: str = '!',
        self_bot: bool = True,
        owner_id: Optional[Union[int, str]] = None,
        owner_ids: Optional[Set[Union[int, str]]] = None,
        **kwargs
    ):
        super().__init__(token, **kwargs)
        self.command_prefix = command_prefix
        self.self_bot = self_bot
        self.owner_id = str(owner_id) if owner_id is not None else None
        self.owner_ids: Set[str] = {str(o) for o in owner_ids} if owner_ids else set()
        if self.owner_id:
            self.owner_ids.add(self.owner_id)
        self.commands: Dict[str, Callable] = {}
        self.dispatcher.register('on_message', self._on_message)

    def command(self, name: Optional[str] = None, *, checks: Optional[List[Callable]] = None):
        def decorator(func: Callable):
            cmd_name = name or getattr(func, '__command_name__', func.__name__)
            cmd_checks = getattr(func, '__command_checks__', [])[:]
            if checks:
                cmd_checks.extend(checks)
            func.__command_checks__ = cmd_checks
            self.commands[cmd_name] = func
            return func
        return decorator

    async def _on_message(self, message):
        author_id = str(message.author.id) if (message and getattr(message, 'author', None)) else None
        user_id = str(self.user.id) if (self.user and getattr(self.user, 'id', None)) else None

        if self.self_bot:
            if user_id and author_id != user_id and author_id not in self.owner_ids:
                return
        else:
            if user_id and author_id == user_id:
                return

        if not getattr(message, 'content', None) or not message.content.startswith(self.command_prefix):
            return

        content = message.content[len(self.command_prefix):]
        if not content:
            return

        parts = content.split()
        command_name = parts[0].lower()
        args = parts[1:]

        command = self.commands.get(command_name)
        if not command:
            return

        ctx = Context(self, message, command_prefix=self.command_prefix)

        try:
            checks = getattr(command, '__command_checks__', [])
            for chk in checks:
                res = chk(ctx)
                if asyncio.iscoroutine(res):
                    res = await res
                if not res:
                    raise CheckFailure(f"Check failed for command '{command_name}'")
            await command(ctx, *args)
        except Exception as e:
            await self.on_command_error(ctx, e)

    async def on_command_error(self, ctx: Context, error: Exception):
        pass
