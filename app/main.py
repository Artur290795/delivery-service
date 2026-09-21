from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends

from app.schemas.parcel import ParcelCreate
from app.api.dependencies import get_session
from app.services.parcel import ParcelService

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, world!"}


@app.post("/parcels")
async def create_parcel(
    parcel: ParcelCreate, session: AsyncSession = Depends(get_session)
):
    new_parcel = await ParcelService.create(session, parcel)
    return new_parcel
