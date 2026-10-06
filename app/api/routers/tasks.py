from fastapi import APIRouter

from app.tasks import calculate_delivery_costs_task

router = APIRouter()

@router.post("/tasks/delivery-cost/calculate")
def trigger_delivery_cost_calculation():
    calculate_delivery_costs_task.delay()
    return {"status": "started"}
