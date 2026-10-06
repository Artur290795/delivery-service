from fastapi import APIRouter, Depends

from app.api.dependencies import get_support_service
from app.schemas import SupportRequest
from app.services import SupportService

router = APIRouter()


@router.post("/support")
async def get_support(
    support_req: SupportRequest,
    support_service: SupportService = Depends(get_support_service),
) -> str:
    return await support_service.get_answer(support_req.question)
