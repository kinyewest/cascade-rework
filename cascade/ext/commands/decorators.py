from typing import Callable, Optional, List


def command(name: Optional[str] = None, *, checks: Optional[List[Callable]] = None):
    def decorator(func: Callable):
        func.__command_name__ = name or func.__name__
        existing = getattr(func, '__command_checks__', [])
        if checks:
            existing = list(existing) + list(checks)
        func.__command_checks__ = existing
        return func
    return decorator


def check(predicate: Callable):
    def decorator(func: Callable):
        if not hasattr(func, '__command_checks__'):
            func.__command_checks__ = []
        func.__command_checks__.append(predicate)
        return func
    return decorator
