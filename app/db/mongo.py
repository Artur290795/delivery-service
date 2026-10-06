from pymongo import AsyncMongoClient

MONGO_URL = "mongodb://localhost:27017"

client = AsyncMongoClient(MONGO_URL)

db = client["delivery_service"]


def get_delivery_cost_log_collection():
    return db["delivery_cost_logs"]
