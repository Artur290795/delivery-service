"""Фоновая Celery-задача асинхронной регистрации посылки."""

import asyncio
import httpx
from loguru import logger

from redis.asyncio import Redis

from app.clients import CBRClient
from app.config import settings
from app.db import async_session_maker, get_delivery_cost_log_collection
from app.repositories import DeliveryCostLogRepository
from app.schemas import ParcelCreate
from app.services import DeliveryCostLogService, ParcelService
from app.celery_app import celery_app


@celery_app.task
def register_parcel_task(parcel_data: dict, session_id: str) -> int:
    logger.info("Parcel registration task started")
    try:
        parcel_id = asyncio.run(register_parcel(parcel_data, session_id))
    except Exception:
        logger.exception("Parcel registration task failed")
        raise
    logger.info(
        "Parcel registration task completed: parcel_id={parcel_id}",
        parcel_id=parcel_id,
    )
    return parcel_id


async def register_parcel(parcel_data: dict, session_id: str) -> int:
    parcel = ParcelCreate.model_validate(parcel_data)
    collection = get_delivery_cost_log_collection()
    log_service = DeliveryCostLogService(
        DeliveryCostLogRepository(collection),
    )
    async with Redis.from_url(settings.redis_url) as cache:
        async with httpx.AsyncClient(timeout=settings.http_timeout_seconds) as client:
            async with async_session_maker() as session:
                result = await ParcelService.create_calculated(
                    session=session,
                    parcel_create=parcel,
                    session_id=session_id,
                    cache=cache,
                    rate_provider=CBRClient(client),
                    delivery_cost_log_service=log_service,
                )
                return result
