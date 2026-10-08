"""Схемы запросов пользовательской поддержки."""

from pydantic import BaseModel


class SupportRequest(BaseModel):
    """Запрос пользователя к AI-поддержке."""
    question: str
