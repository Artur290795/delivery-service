from fastapi import APIRouter

from app.tasks.delivery_cost import calculate_delivery_costs_task

task_router = APIRouter()

@task_router.post("/tasks/delivery-cost/calculate")
def trigger_delivery_cost_calculation():
    calculate_delivery_costs_task.delay()
    return {"status": "started"}
