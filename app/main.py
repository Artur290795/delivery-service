from app.schemas.parcel import ParcelCreate
from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, world!"}


@app.post("/parcels")
async def create_parcel(parcel: ParcelCreate):
    return parcel
