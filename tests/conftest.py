from app.db.mongo import db
import pytest


@pytest.fixture
def get_test_delivery_cost_logs_collection():
    return db["test_delivery_cost_logs"]
