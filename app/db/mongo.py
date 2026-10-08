from pymongo import AsyncMongoClient

from app.config import settings

client = AsyncMongoClient(settings.mongo_url)
db = client[settings.mongo_database_name]


def get_delivery_cost_log_collection():
    return db["delivery_cost_logs"]
