from typing import Optional, Union


def is_owner(user_id: Optional[Union[int, str]] = None):
    def predicate(ctx):
        if not getattr(ctx, 'author', None):
            return False
        author_id = str(ctx.author.id)
        if user_id is not None:
            return author_id == str(user_id)
        bot = getattr(ctx, 'bot', None)
        if bot:
            owner_ids = getattr(bot, 'owner_ids', None)
            if owner_ids and author_id in {str(o) for o in owner_ids}:
                return True
            owner_id = getattr(bot, 'owner_id', None)
            if owner_id is not None and author_id == str(owner_id):
                return True
            user = getattr(bot, 'user', None)
            if user and hasattr(user, 'id') and author_id == str(user.id):
                return True
        return False
    return predicate


def is_guild():
    def predicate(ctx):
        return getattr(ctx, 'guild', None) is not None
    return predicate


def is_dm():
    def predicate(ctx):
        return getattr(ctx, 'guild', None) is None
    return predicate


def has_role(role_id: Union[int, str]):
    def predicate(ctx):
        guild = getattr(ctx, 'guild', None)
        if not guild or not getattr(ctx, 'author', None):
            return False
        member = guild.get_member(ctx.author.id)
        if not member or not hasattr(member, 'roles'):
            return False
        target = str(role_id)
        return any(str(r) == target for r in member.roles)
    return predicate


def has_any_role(*role_ids: Union[int, str]):
    def predicate(ctx):
        guild = getattr(ctx, 'guild', None)
        if not guild or not getattr(ctx, 'author', None):
            return False
        member = guild.get_member(ctx.author.id)
        if not member or not hasattr(member, 'roles'):
            return False
        target_roles = {str(r) for r in role_ids}
        return any(str(r) in target_roles for r in member.roles)
    return predicate
