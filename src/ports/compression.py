from abc import ABC, abstractmethod


class ICompressionProvider(ABC):
    @abstractmethod
    async def unarchive(self, data: bytes, out_path: str, type: str) -> str:
        raise NotImplementedError
