import os
import shutil

import aiofiles

from src.ports.storage import IStorageProvider


class FSStorageProvider(IStorageProvider):
    def __init__(self, base_path: str, projects_base_path: str) -> None:
        self.base_path = base_path
        self.projects_base_path = projects_base_path

        os.makedirs(base_path, exist_ok=True)
        os.makedirs(projects_base_path, exist_ok=True)

    async def write(self, path: str, data: bytes) -> None:
        path = os.path.join(self.base_path, path)
        async with aiofiles.open(path, mode="wb") as f:
            await f.write(data)

    async def read(self, path: str) -> bytes:
        path = os.path.join(self.base_path, path)
        async with aiofiles.open(path, mode="rb") as f:
            return await f.read()

    async def read_lines(self, path: str) -> list[str]:
        async with aiofiles.open(path) as f:
            return await f.readlines()

    async def delete(self, path: str) -> None:
        path = os.path.join(self.base_path, path)
        project_path = os.path.join(self.projects_base_path, path.split(".", 1)[0])
        if os.path.isdir(project_path):
            shutil.rmtree(project_path)
            return

        os.remove(path)

    async def exists(self, path: str) -> bool:
        return os.path.exists(os.path.join(self.base_path, path))
