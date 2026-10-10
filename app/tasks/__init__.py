"""Экспорт фоновых задач Celery."""

from app.tasks.parcel_registration import register_parcel_task

__all__ = ["register_parcel_task"]
