import os
import shutil

import aiofiles

from src.ports.storage import IStorageProvider


class FSStorageProvider(IStorageProvider):
    def __init__(self, base_path: str) -> None:
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    async def write(self, path: str, data: bytes) -> None:
        path = os.path.join(self.base_path, path)
        async with aiofiles.open(path, mode="wb") as f:
            await f.write(data)

    async def read(self, path: str) -> bytes:
        path = os.path.join(self.base_path, path)
        async with aiofiles.open(path, mode="rb") as f:
            return await f.read()

    async def delete(self, path: str) -> None:
        path = os.path.join(self.base_path, path)
        if os.path.isdir(path):
            shutil.rmtree(path)
            return

        os.remove(path)

    async def exists(self, path: str) -> bool:
        return os.path.exists(os.path.join(self.base_path, path))
