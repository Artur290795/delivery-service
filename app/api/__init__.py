from app.api.dependencies import (
    get_delivery_cost_log_service,
    get_http_client,
    get_session,
    get_support_service,
)

from app.api.routers import (
    task_router,
    delivery_costs_router,
    parcel_router,
    parcel_types_router,
    support_router,
)
