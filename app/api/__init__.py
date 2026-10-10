"""Пакет HTTP API сервиса доставки."""

from app.api.dependencies import (
    get_delivery_cost_log_service,
    get_http_client,
    get_session,
    get_support_service,
)
from app.api.routers import router

__all__ = [
    "get_delivery_cost_log_service",
    "get_http_client",
    "get_session",
    "get_support_service",
    "router",
]
