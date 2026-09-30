from fastapi import APIRouter, Depends

from app.api.dependencies import get_support_service
from app.schemas.support import SupportRequest
from app.services.support import SupportService

router = APIRouter()


@router.post("/support")
async def get_support(
    support_req: SupportRequest,
    support_service: SupportService = Depends(get_support_service),
) -> list[float]:
    return await support_service.get_question(support_req.question)


@router.get("/text-search")
async def text_search(request: Request):
    pass