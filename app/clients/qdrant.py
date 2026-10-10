"""Клиент векторного хранилища Qdrant."""

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import Distance, PointStruct, ScoredPoint, VectorParams

from app.config import settings


class QdrantClient:
    """Клиент Qdrant для хранения и поиска векторных документов."""

    def __init__(self):
        self.client = AsyncQdrantClient(url=settings.qdrant_url)
        self.collection_name = settings.qdrant_collection_name

    async def add_points(self, points: list[PointStruct]) -> None:
        await self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    async def search_similar(self, vector: list[float]) -> ScoredPoint | None:
        results = await self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=1,
        )
        if results.points:
            return results.points[0]

        return None

    async def ensure_collection(self):
        try:
            await self.client.get_collection(self.collection_name)
        except UnexpectedResponse as exc:
            if exc.status_code == 404:
                await self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=384,
                        distance=Distance.COSINE,
                    ),
                )
            else:
                raise

    async def recreate_collection(self):
        await self.client.delete_collection(self.collection_name)
        await self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )
