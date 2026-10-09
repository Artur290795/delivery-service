"""Асинхронное подключение и фабрика сессий PostgreSQL."""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,
    poolclass=NullPool,
)
async_session_maker = async_sessionmaker(engine)
