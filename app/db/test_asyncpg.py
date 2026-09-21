import asyncio
import asyncpg


async def check_connection():
    conn = await asyncpg.connect(
    user="delivery_user",
    password="delivery_password",
    database="delivery_service",
    host="localhost",
    port=5433,
    ssl=False,
    )
    result = await conn.fetchval("SELECT 1")
    await conn.close()
    return result


print(asyncio.run(check_connection()))