import pytest_asyncio

from app.db.mongo import db


@pytest_asyncio.fixture
async def get_test_delivery_cost_logs_collection():
    collection = db["test_delivery_cost_logs"]

    await collection.delete_many({})

    yield collection
