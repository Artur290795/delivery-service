import asyncio

from app.clients.qdrant import QdrantService


async def main():
    qdrant = QdrantService()

    await qdrant.client.delete_collection(collection_name=qdrant._COLLECTION_NAME)


if __name__ == "__main__":
    asyncio.run(main())

