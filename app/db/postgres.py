import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)


async def test_connection():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
    return result.scalar()

print(asyncio.run(test_connection()))