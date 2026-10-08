from celery import Celery
from app.config import settings

celery_app = Celery(
    "delivery_service",
    broker=settings.rabbitmq_url,
    include=["app.tasks.parcel_registration"],
)
