"""Создание и проверка пользовательских сессий в Redis."""

import secrets
from app.cache import redis
from app.config import settings

async def create_session() -> str:
    session_id = secrets.token_urlsafe(32)
    redis_key = f"session:{session_id}"
    await redis.set(redis_key, 1, ex=settings.session_ttl_seconds)
    return session_id


async def session_exists(session_id: str) -> bool:
    redis_key = f"session:{session_id}"
    value = await redis.get(redis_key)
    return value is not None
