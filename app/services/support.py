from app.services.embedding import EmbeddingService
from app.clients.qdrant import QdrantService


class SupportService:
    def __init__(self, emb_service: EmbeddingService, qdrant_service: QdrantService):
        self.emb_service = emb_service
        self.qdrant_service = qdrant_service

    async def get_question(self, question: str) -> list[str]:
        vector = self.emb_service.convert_text_to_vector(question)
        similars = await self.qdrant_service.search_similar(vector)
        llm_context = [similar.payload["text"] for similar in similars]
        return llm_context
