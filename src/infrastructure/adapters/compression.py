import asyncio
import os
import tarfile
import zipfile
from io import BytesIO

from src.ports.compression import ICompressionProvider


class FSCompressionProvider(ICompressionProvider):
    def __init__(self, base_path: str) -> None:
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    async def unarchive(self, data: bytes, out_path: str, type: str) -> None:
        if type.startswith("zip"):
            with zipfile.ZipFile(file=BytesIO(data), mode="r") as zf:
                await asyncio.to_thread(zf.extractall, out_path)
        elif type.startswith("tar"):
            with tarfile.TarFile(name=data, mode="r") as tf:
                await asyncio.to_thread(tf.extractall, out_path)
