"""Зависимости FastAPI для доступа к инфраструктуре и сервисам."""

from fastapi import FastAPI, Request
import httpx

from app.clients import QdrantClient
from app.config import settings
from app.db import async_session_maker, get_delivery_cost_log_collection, mongo_client
from app.rag import IngestionService
from app.repositories import DeliveryCostLogRepository
from app.services import (
    DeliveryCostLogService,
    EmbeddingService,
    LLMService,
    SupportService,
)

# FastAPI dependencies


async def get_session():
    async with async_session_maker() as session:
        yield session


async def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


def get_support_service(request: Request) -> SupportService:
    return request.app.state.support_service


def get_delivery_cost_log_service(
    request: Request,
) -> DeliveryCostLogService:
    return request.app.state.delivery_cost_log_service


# Application dependency initialization


async def init_http_client(app: FastAPI) -> None:
    app.state.http_client = httpx.AsyncClient(
        timeout=settings.http_timeout_seconds,
    )


def init_embedding_service(app: FastAPI) -> None:
    app.state.emb_service = EmbeddingService()


async def init_qdrant_client(app: FastAPI) -> None:
    qdrant_client = QdrantClient()
    await qdrant_client.ensure_collection()
    app.state.qdrant_client = qdrant_client


def init_ingestion_service(app: FastAPI) -> None:
    app.state.ingestion_service = IngestionService(
        app.state.emb_service,
        app.state.qdrant_client,
    )


def init_support_service(app: FastAPI) -> None:
    llm_service = LLMService(
        api_key=settings.yandex_api_key,
        folder_id=settings.yandex_folder_id,
    )
    app.state.llm_service = llm_service

    app.state.support_service = SupportService(
        app.state.emb_service,
        app.state.qdrant_client,
        llm_service,
    )


async def init_delivery_cost_log_service(app: FastAPI) -> None:
    collection = get_delivery_cost_log_collection()
    await collection.create_index(
        [("parcel_id", 1)],
        unique=True,
    )

    repository = DeliveryCostLogRepository(collection)
    app.state.delivery_cost_log_service = DeliveryCostLogService(repository)


async def init_dependencies(app: FastAPI) -> None:
    await init_http_client(app)
    init_embedding_service(app)
    await init_qdrant_client(app)
    init_ingestion_service(app)
    init_support_service(app)
    await init_delivery_cost_log_service(app)


async def release_clients(app: FastAPI) -> None:
    await app.state.http_client.aclose()
    await mongo_client.aclose()
