from uuid import uuid4

from qdrant_client.models import PointStruct
from app.services.embedding import EmbeddingService
from app.clients.qdrant import QdrantService
from app.rag.chunking import split_text
# если больше нигде не использую split_text надо его сюда зафигачить как статикметод

class IngestionService:
    def __init__(self, emb_service: EmbeddingService, qdrant_service: QdrantService):
        self.emb_service = emb_service
        self.qdrant_service = qdrant_service

    async def ingest(self, document: str):
        print(123)
        chunks = split_text(document)
        print("DOCUMENT:")
        print(document)

        print("CHUNKS:")
        
        for chunk in chunks:
            print(repr(chunk))

        vectors = [self.emb_service.convert_text_to_vector(chunk) for chunk in chunks]
        points = []
        for (chunk, vector) in zip(chunks, vectors):
            point = PointStruct(id=uuid4(), vector=vector, payload={"text": chunk})
            points.append(point)
        await self.qdrant_service.add_points(points)
