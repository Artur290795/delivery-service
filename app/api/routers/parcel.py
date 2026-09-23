from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_session
from app.schemas.parcel import ParcelCreate, ParcelCreateResponse, ParcelResponse, ParcelType
from app.services.parcel import ParcelService

router = APIRouter()


@router.post("/parcels", response_model=ParcelCreateResponse)
async def create_parcel(
    request: Request, parcel: ParcelCreate, session: AsyncSession = Depends(get_session)
):
    session_id = request.state.session_id
    new_parcel = await ParcelService.create(session, parcel, session_id)
    return new_parcel


@router.get("/parcels", response_model=list[ParcelResponse])
async def get_parcels(
    request: Request,
    session: AsyncSession = Depends(get_session),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    parcel_type: ParcelType | None = Query(default=None),
    delivery_cost_calculated: bool | None = Query(default=None)
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
    parcel_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session)
) -> ParcelResponse | None:
    parcel = await ParcelService.get_parcel_by_id(session, parcel_id, request.state.session_id)
    return parcel