from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_session
from app.schemas import (
    ParcelCreate,
    ParcelCreateResponse,
    ParcelResponse,
    ParcelType,
)
from app.services import ParcelService
from app.tasks.parcel_registration import register_parcel_task

router = APIRouter()


@router.post(
    "/parcels", response_model=ParcelCreateResponse, status_code=status.HTTP_202_ACCEPTED
)
async def create_parcel(request: Request, parcel: ParcelCreate):
    task = register_parcel_task.delay(
        parcel.model_dump(mode="json"), request.state.session_id
    )
    return ParcelCreateResponse(status="accepted", task_id=task.id)


@router.get("/parcels", response_model=list[ParcelResponse])
async def get_parcels(
    request: Request,
    session: AsyncSession = Depends(get_session),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    parcel_type: ParcelType | None = Query(default=None),
    delivery_cost_calculated: bool | None = Query(default=None),
):
    parcels = await ParcelService.get_user_parcels(
        session,
        session_id=request.state.session_id,
        limit=limit,
        offset=offset,
        parcel_type=parcel_type,
        delivery_cost_calculated=delivery_cost_calculated,
    )
    return parcels


@router.get("/parcels/{parcel_id}", response_model=ParcelResponse)
async def get_parcel(
    parcel_id: int, request: Request, session: AsyncSession = Depends(get_session)
) -> ParcelResponse | None:
    parcel = await ParcelService.get_parcel_by_id(
        session, parcel_id, request.state.session_id
    )
    return parcel
