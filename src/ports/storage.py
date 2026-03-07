from abc import ABC, abstractmethod


class IStorageProvider(ABC):
    @abstractmethod
    async def write(self, path: str, data: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    async def read(self, path: str) -> bytes:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, path: str) -> bool:
        raise NotImplementedError
