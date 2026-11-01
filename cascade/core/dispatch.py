import asyncio
from typing import Dict, List, Callable, Any, Optional, Tuple


class EventDispatcher:
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
        self._waiters: Dict[str, List[Tuple[asyncio.Future, Optional[Callable]]]] = {}

    def register(self, event: str, callback: Callable) -> None:
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def unregister(self, event: str, callback: Callable) -> None:
        if event in self._listeners:
            try:
                self._listeners[event].remove(callback)
            except ValueError:
                pass

    def dispatch(self, event: str, *args, **kwargs) -> None:
        if event in self._listeners:
            for callback in self._listeners[event]:
                asyncio.create_task(self._execute_callback(callback, *args, **kwargs))
        
        if event in self._waiters:
            remaining = []
            for entry in self._waiters[event]:
                future, check = entry
                if future.done():
                    continue
                matched = True
                if check is not None:
                    try:
                        matched = bool(check(*args, **kwargs))
                    except Exception:
                        matched = False
                if matched:
                    future.set_result((args, kwargs))
                else:
                    remaining.append(entry)
            if remaining:
                self._waiters[event] = remaining
            else:
                self._waiters.pop(event, None)

    async def _execute_callback(self, callback: Callable, *args, **kwargs) -> None:
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(*args, **kwargs)
            else:
                callback(*args, **kwargs)
        except Exception:
            pass

    async def wait_for(self, event: str, check: Optional[Callable] = None, timeout: Optional[float] = None) -> Any:
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        
        entry = (future, check)
        if event not in self._waiters:
            self._waiters[event] = []
        self._waiters[event].append(entry)

        try:
            args, kwargs = await asyncio.wait_for(future, timeout=timeout)
            return args[0] if len(args) == 1 else args
        finally:
            if event in self._waiters:
                try:
                    self._waiters[event].remove(entry)
                    if not self._waiters[event]:
                        self._waiters.pop(event, None)
                except ValueError:
                    pass
