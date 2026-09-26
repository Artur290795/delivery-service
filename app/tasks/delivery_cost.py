import asyncio

import httpx
from redis.asyncio import Redis

from app.clients.cbr import CBRClient
from app.celery_app import celery_app
from app.db.postgres import async_session_maker
from app.services.delivery_cost import DeliveryCostService


@celery_app.task
def calculate_delivery_costs_task() -> None:
    asyncio.run(calculate_delivery_costs())


async def calculate_delivery_costs() -> None:
    async with Redis(host="localhost", port=6379) as cache:
        async with httpx.AsyncClient() as client:
            async with async_session_maker() as session:
                await DeliveryCostService.calculate_delivery_costs(
                    cache=cache,
                    rate_provider=CBRClient(client),
                    session=session,
                )
