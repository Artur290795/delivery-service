from pydantic import BaseModel


class SupportRequest(BaseModel):
    question: str
