from abc import ABC, abstractmethod
from typing import Any


class IDBProvider(ABC):
    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def insert(self, collection_name: str, data: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, collection_name: str, id: str, data: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, collection_name: str, **kwargs) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        collection_name: str,
        limit: int = 0,
        offset: int = 0,
        orderings: list[str] | None = None,
        **kwargs,
    ) -> list[dict[str, Any]]:
        raise NotImplementedError
