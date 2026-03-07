from abc import ABC, abstractmethod


class IRepository[DE: object](ABC):
    collection_name: str

    @abstractmethod
    async def get(self, **kwargs) -> DE | None:
        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        limit: int = 0,
        offset: int = 0,
        orderings: list[str] | None = None,
        **kwargs,
    ) -> list[DE]:
        raise NotImplementedError

    @abstractmethod
    async def save(self, entity: DE) -> None:
        raise NotImplementedError
