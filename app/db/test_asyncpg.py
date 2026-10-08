import asyncio

import asyncpg

from app.config import settings


async def check_connection():
    database_url = settings.database_url.replace(
        "postgresql+asyncpg://", "postgresql://", 1
    )
    conn = await asyncpg.connect(database_url, ssl=False)
    result = await conn.fetchval("SELECT 1")
    await conn.close()
    return result


print(asyncio.run(check_connection()))