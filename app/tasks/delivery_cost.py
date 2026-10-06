import asyncio

import httpx
from redis.asyncio import Redis

from app.clients import CBRClient
from app.celery_app import celery_app
from app.db import async_session_maker, get_delivery_cost_log_collection
from app.services import DeliveryCostService, DeliveryCostLogService
from app.repositories import DeliveryCostLogRepository


@celery_app.task
def calculate_delivery_costs_task() -> None:
    asyncio.run(calculate_delivery_costs())


async def calculate_delivery_costs() -> None:
    collection = get_delivery_cost_log_collection()
    delivery_cost_log_repo = DeliveryCostLogRepository(collection)
    delivery_cost_log_service = DeliveryCostLogService(delivery_cost_log_repo)

    async with Redis(host="localhost", port=6379) as cache:
        async with httpx.AsyncClient() as client:
            async with async_session_maker() as session:
                await DeliveryCostService.calculate_delivery_costs(
                    cache=cache,
                    rate_provider=CBRClient(client),
                    session=session,
                    delivery_cost_log_service=delivery_cost_log_service,
                )
