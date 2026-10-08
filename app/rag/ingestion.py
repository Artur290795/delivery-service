"""Загрузка документов и эмбеддингов в Qdrant."""

from uuid import uuid4

from qdrant_client.models import PointStruct
from loguru import logger
from app.services import EmbeddingService
from app.clients import QdrantClient
from app.rag.chunking import split_text
# если больше нигде не использую split_text надо его сюда зафигачить как статикметод

class IngestionService:
    """Сервис загрузки текстов в векторную базу знаний."""
    def __init__(self, emb_service: EmbeddingService, qdrant_client: QdrantClient):
        self.emb_service = emb_service
        self.qdrant_client = qdrant_client

    async def ingest(self, document: str):
        chunks = split_text(document)
        logger.info("Document split into chunks: chunk_count={chunk_count}", chunk_count=len(chunks))

        vectors = [self.emb_service.convert_text_to_vector(chunk) for chunk in chunks]
        points = []
        for (chunk, vector) in zip(chunks, vectors):
            point = PointStruct(id=uuid4(), vector=vector, payload={"text": chunk})
            points.append(point)
        await self.qdrant_client.add_points(points)
        logger.info("Document ingested into Qdrant: point_count={point_count}", point_count=len(points))
