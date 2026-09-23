from celery import Celery

celery_app = Celery(
    "delivery_service",
    broker="redis://localhost:6379/0",
    include=["app.tasks.delivery_cost"],
)


celery_app.conf.beat_schedule = {
    "calculate-delivery-costs": {
        "task": "app.tasks.delivery_cost.calculate_delivery_costs_task",
        "schedule": 300.0,  # 5 минут
    },
}
