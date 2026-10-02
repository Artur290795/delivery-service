from fastapi import status, Request
from fastapi.responses import JSONResponse
from app.exceptions.base import ParcelNotFoundException



async def parcel_not_found_exception_handler(request : Request, exc: ParcelNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


