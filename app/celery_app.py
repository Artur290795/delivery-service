"""Конфигурация Celery и подключения к очереди RabbitMQ."""

from celery import Celery
from app.config import settings
from app.logging import configure_logging

configure_logging()

celery_app = Celery(
    "delivery_service",
    broker=settings.rabbitmq_url,
    include=["app.tasks.parcel_registration"],
)
