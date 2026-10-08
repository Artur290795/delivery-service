import asyncio

from app.clients import QdrantClient


async def main():
    qdrant = QdrantClient()

    await qdrant.client.delete_collection(collection_name=qdrant._COLLECTION_NAME)


if __name__ == "__main__":
    asyncio.run(main())
