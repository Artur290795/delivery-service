from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import httpx
from app.exceptions import parcel_not_found_exception_handler, ParcelNotFoundException
from app.sessions.session import create_session, session_exists
from app.api.routers.parcel_types import router as parcel_types_router
from app.api.routers.parcel import router as parcel_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = httpx.AsyncClient()
    app.state.http_client = client
    yield
    await client.aclose()


app = FastAPI(lifespan=lifespan)
app.include_router(parcel_types_router)
app.include_router(parcel_router)
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
