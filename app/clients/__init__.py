"""Клиенты внешних сервисов."""

from app.clients.cbr import CBRClient
from app.clients.qdrant import QdrantClient

__all__ = ["CBRClient", "QdrantClient"]
