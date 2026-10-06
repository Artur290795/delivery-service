import asyncio

import httpx
from redis.asyncio import Redis

from app.clients.cbr import CBRClient
from app.celery_app import celery_app
from app.db.postgres import async_session_maker
from app.services.delivery_cost import DeliveryCostService
from app.repositories.delivery_cost import DeliveryCostLogRepository
from app.services.delivery_cost_log import DeliveryCostLogService
from app.db.mongo import get_delivery_cost_log_collection


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
