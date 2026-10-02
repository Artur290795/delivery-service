from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, ScoredPoint
from qdrant_client.http.exceptions import UnexpectedResponse


class QdrantService:
    _COLLECTION_NAME = "delivery_knowledge"

    def __init__(self):
        self.client = AsyncQdrantClient(
            host="localhost",
            port=6333,
        )

    async def add_points(self, points: list[PointStruct]) -> None:
        await self.client.upsert(
            collection_name=self._COLLECTION_NAME,
            points=points,
        )

    async def search_similar(self, vector: list[float]) -> ScoredPoint | None:
        results = await self.client.query_points(
            collection_name=self._COLLECTION_NAME,
            query=vector,
            limit=1,
        )
        if results.points:
            return results.points[0]

        return None

    async def ensure_collection(self):
        try:
            await self.client.get_collection(self._COLLECTION_NAME)
        except UnexpectedResponse as exc:
            if exc.status_code == 404:
                await self.client.create_collection(
                    collection_name=self._COLLECTION_NAME,
                    vectors_config=VectorParams(
                        size=384,
                        distance=Distance.COSINE,
                    ),
                )
            else:
                raise

    async def recreate_collection(self):
        await self.client.delete_collection(self._COLLECTION_NAME)

        await self.client.create_collection(
            collection_name=self._COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )
