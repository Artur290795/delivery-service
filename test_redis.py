import asyncio

from app.cache.redis import redis


async def main():
    result = await redis.ping()
    print(result)


asyncio.run(main())