import httpx
from fastapi import Request
from app.db.postgres import async_session_maker
from app.services.support import SupportService

async def get_session():
    async with async_session_maker() as session:
        yield session

async def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


def get_support_service(request: Request) -> SupportService:
    return request.app.state.support_service