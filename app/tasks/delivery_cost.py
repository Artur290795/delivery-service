import asyncio

import httpx

from app.celery_app import celery_app
from app.db.postgres import async_session_maker
from app.services.delivery_cost import DeliveryCostService



@celery_app.task
def calculate_delivery_costs_task():
    asyncio.run(calculate_delivery_costs())


async def calculate_delivery_costs() -> None:
    async with httpx.AsyncClient() as client:
        async with async_session_maker() as session:
            await DeliveryCostService.calculate_delivery_costs(client, session)