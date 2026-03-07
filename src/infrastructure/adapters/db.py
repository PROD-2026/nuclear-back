from typing import Any

import pymongo
from pymongo import AsyncMongoClient

from src.ports.db import IDBProvider


class MongoDBProvider(IDBProvider):
    def __init__(self, connection_uri: str, database: str) -> None:
        self._mongo = AsyncMongoClient(connection_uri)
        self._db = self._mongo[database]

    async def connect(self) -> None:
        await self._mongo.admin.command({"ping": 1})

    async def close(self) -> None:
        await self._mongo.close()

    async def insert(self, collection_name: str, data: dict[str, Any]) -> None:
        if "id" in data.keys():
            data["_id"] = str(data.pop("id"))

        collection = self._db[collection_name]
        await collection.insert_one(data)

    async def update(self, collection_name: str, id: str, data: dict[str, Any]) -> None:
        if "id" in data.keys():
            data["_id"] = str(data.pop("id"))

        collection = self._db[collection_name]
        await collection.replace_one(filter={"_id": str(id)}, replacement=data)

    async def get(self, collection_name: str, **kwargs) -> dict[str, Any] | None:
        if "id" in kwargs.keys():
            kwargs["_id"] = str(kwargs.pop("id"))

        collection = self._db[collection_name]
        data: dict | None = await collection.find_one(filter=kwargs)
        if not data:
            return

        data["id"] = str(data.pop("_id"))

        return data

    async def list(
        self,
        collection_name: str,
        limit: int = 0,
        offset: int = 0,
        orderings: list[str] | None = None,
        **kwargs,
    ) -> list[dict[str, Any]]:
        if "id" in kwargs.keys():
            kwargs["_id"] = str(kwargs.pop("id"))

        collection = self._db[collection_name]

        query = (
            collection.find(kwargs)
            .sort(
                [
                    (
                        ordering.lstrip("-"),
                        pymongo.DESCENDING if ordering[0] == "-" else pymongo.ASCENDING,
                    )
                    for ordering in (orderings or [])
                ]
            )
            .skip(offset)
        )
        if limit > 0:
            query = query.limit(limit)

        documents = []
        async for doc in query:
            doc["id"] = str(doc.pop("_id"))
            documents.append(doc)

        return documents
