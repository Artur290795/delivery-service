from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import httpx
from app.exceptions import parcel_not_found_exception_handler, ParcelNotFoundException
from app.sessions.session import create_session, session_exists
from app.api.routers.parcel_types import router as parcel_types_router
from app.api.routers.parcel import router as parcel_router
from app.api.routers.tasks import task_router
from app.api.routers.support import router as support_router
from app.services.support import SupportService
from app.services.embedding import EmbeddingService
from app.services.llm import LLMService
from app.clients.qdrant import QdrantService
from app.rag.ingestion import IngestionService
from app.config import settings
# DOCUMENT = """
# Доставка одежды осуществляется по России.
# Стоимость доставки зависит от веса посылки и стоимости содержимого.
# Для получения помощи обратитесь в службу поддержки.
# """


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = httpx.AsyncClient()
    app.state.http_client = client

    emb_service = EmbeddingService()
    app.state.emb_service = emb_service

    qdrant_service = QdrantService()
    await qdrant_service.ensure_collection()
    app.state.qdrant_service = qdrant_service

    ingestion_service = IngestionService(emb_service, qdrant_service)
    app.state.ingestion_service = ingestion_service
    # await ingestion_service.ingest(DOCUMENT)
    llm_service = LLMService(api_key=settings.openai_api_key)
    support_service = SupportService(emb_service, qdrant_service, llm_service)
    app.state.support_service = support_service

    yield
    await client.aclose()


app = FastAPI(lifespan=lifespan)
app.include_router(parcel_types_router)
app.include_router(parcel_router)
app.include_router(task_router)
app.include_router(support_router)
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
