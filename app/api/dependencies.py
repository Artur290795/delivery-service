import httpx
from fastapi import Request
from app.db.postgres import async_session_maker

async def get_session():
    async with async_session_maker() as session:
        yield session

async def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client