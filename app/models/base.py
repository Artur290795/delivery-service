"""Базовый класс SQLAlchemy ORM-моделей."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый декларативный класс для всех SQLAlchemy ORM-моделей."""
    pass
