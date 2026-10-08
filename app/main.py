"""Точка входа FastAPI-приложения сервиса доставки."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import httpx
from loguru import logger

from app.exceptions import parcel_not_found_exception_handler, ParcelNotFoundException
from app.repositories import DeliveryCostLogRepository
from app.services import (
    DeliveryCostLogService,
    SupportService,
    EmbeddingService,
    LLMService,
)
from app.sessions import create_session, session_exists
from app.api import (
    parcel_types_router,
    parcel_router,
    support_router,
    delivery_costs_router,
)
from app.clients import QdrantClient
from app.rag import IngestionService
from app.db import get_delivery_cost_log_collection, mongo_client
from app.config import settings

# DOCUMENT = """
# Доставка одежды осуществляется по России.
# Стоимость доставки зависит от веса посылки и стоимости содержимого.
# Для получения помощи обратитесь в службу поддержки.
# """


@asynccontextmanager
async def lifespan(app: FastAPI):
    http_client = httpx.AsyncClient(timeout=settings.http_timeout_seconds)
    app.state.http_client = http_client

    emb_service = EmbeddingService()
    app.state.emb_service = emb_service

    qdrant_client = QdrantClient()
    await qdrant_client.ensure_collection()
    app.state.qdrant_client = qdrant_client

    ingestion_service = IngestionService(emb_service, qdrant_client)
    app.state.ingestion_service = ingestion_service
    llm_service = LLMService(
        api_key=settings.yandex_api_key, folder_id=settings.yandex_folder_id
    )
    support_service = SupportService(emb_service, qdrant_client, llm_service)
    app.state.support_service = support_service

    collection = get_delivery_cost_log_collection()
    await collection.create_index(
        [("parcel_id", 1)],
        unique=True,
    )
    delivery_cost_log_repo = DeliveryCostLogRepository(collection)
    app.state.delivery_cost_log_service = DeliveryCostLogService(delivery_cost_log_repo)

    logger.info("Application started successfully")

    yield
    logger.info("Application shutdown started")
    await http_client.aclose()
    await mongo_client.aclose()


app = FastAPI(lifespan=lifespan)
app.include_router(parcel_types_router)
app.include_router(parcel_router)
app.include_router(support_router)
app.include_router(delivery_costs_router)
app.add_exception_handler(ParcelNotFoundException, parcel_not_found_exception_handler)


@app.middleware("http")
async def session_middleware(request: Request, call_next):
    session_id = request.cookies.get("session_id")
    is_new_session = False

    if session_id is None:
        session_id = await create_session()
        is_new_session = True
    elif not await session_exists(session_id):
        session_id = await create_session()
        is_new_session = True

    request.state.session_id = session_id
    response = await call_next(request)
    if is_new_session:
        response.set_cookie("session_id", session_id)
    return response
