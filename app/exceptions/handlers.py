"""Обработчики доменных исключений для FastAPI."""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from loguru import logger


async def parcel_not_found_exception_handler(request: Request, exc: Exception):
    logger.warning("Parcel not found: path={path}", path=request.url.path)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )
