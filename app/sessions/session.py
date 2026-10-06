import secrets
from app.cache import redis

async def create_session() -> str:
    session_id = secrets.token_urlsafe(32)
    expiration_time = 60 * 60 * 24 # сутки
    redis_key = f"session:{session_id}"
    await redis.set(redis_key, 1, ex=expiration_time)
    return session_id


async def session_exists(session_id: str) -> bool:
    redis_key = f"session:{session_id}"
    value = await redis.get(redis_key)
    return value is not None
