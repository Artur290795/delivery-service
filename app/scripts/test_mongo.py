import asyncio
from bson.decimal128 import Decimal128
from datetime import datetime, timezone

from pymongo import AsyncMongoClient


async def test_mongodb():
    client = AsyncMongoClient("mongodb://localhost:27017")
    collection = client["delivery_service"]["delivery_cost_logs"]
    try:
        index_name = await create_indexes(client)
        insert_result = await collection.insert_one(
            {
                "parcel_id": 123,
                "parcel_type": "electronics",
                "delivery_cost": Decimal128("1250.50"),
                "calculated_at": datetime.now(timezone.utc),
            }
        )
        insert_result = await collection.insert_one(
                    {
                        "parcel_id": 123,
                        "parcel_type": "electronics",
                        "delivery_cost": Decimal128("1250.50"),
                        "calculated_at": datetime.now(timezone.utc),
                    }
                )
    finally:
        await client.aclose()

    return insert_result.inserted_id

async def create_indexes(client: AsyncMongoClient):
    collection = client["delivery_service"]["delivery_cost_logs"]
    index_name = await collection.create_index(
        [("parcel_id", 1)],
        unique=True,
    )
    return index_name

print(asyncio.run(test_mongodb()))
