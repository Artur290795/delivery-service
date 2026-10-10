"""Точка входа FastAPI-приложения сервиса доставки."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.api import router as api_router
from app.api.dependencies import init_dependencies, release_clients
from app.exceptions import ParcelNotFoundException, parcel_not_found_exception_handler
from app.middleware import SessionMiddleware

# DOCUMENT = """
# Доставка одежды осуществляется по России.
# Стоимость доставки зависит от веса посылки и стоимости содержимого.
# Для получения помощи обратитесь в службу поддержки.
# """


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_dependencies(app)

    logger.info("Application started successfully")

    yield
    logger.info("Application shutdown started")
    await release_clients(app)


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
app.add_middleware(SessionMiddleware)
app.add_exception_handler(ParcelNotFoundException, parcel_not_found_exception_handler)
