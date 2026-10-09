"""RAG-сервис поддержки пользователей."""

from app.clients import QdrantClient
from app.services import EmbeddingService, LLMService


class SupportService:
    """Сервис ответов поддержки на основе поиска по базе знаний."""

    _NO_ANSWER_MESSAGE = (
        "Похоже, этот вопрос не относится к службе доставки. "
        "Я могу помочь с вопросами о посылках, доставке и её стоимости."
    )

    def __init__(
        self,
        emb_service: EmbeddingService,
        qdrant_client: QdrantClient,
        llm_service: LLMService,
    ):
        self.emb_service = emb_service
        self.qdrant_client = qdrant_client
        self.llm_service = llm_service

    async def get_answer(self, question: str) -> str:
        vector = self.emb_service.convert_text_to_vector(question)
        similar = await self.qdrant_client.search_similar(vector)
        if similar and similar.score >= 0.6:
            answer = await self.llm_service.generate_answer(
                question,
                similar.payload["text"],  # type: ignore[index]
            )
            return answer
        return self._NO_ANSWER_MESSAGE
