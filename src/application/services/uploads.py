from src.ports.compression import ICompressionProvider
from src.ports.storage import IStorageProvider


class UploadsService:
    def __init__(
        self,
        storage_provider: IStorageProvider,
        compression_provider: ICompressionProvider,
    ) -> None:
        self._storage = storage_provider
        self._compression = compression_provider

    async def upload_project(self, report_id: str, data: bytes) -> None:
        await self._storage.write(path=f"{report_id}.zip", data=data)

    async def unarchive_project(self, report_id: str) -> None:
        if not await self._storage.exists(f"{str(report_id)}.zip"):
            raise FileNotFoundError("Report archive not found")

        data = await self._storage.read(f"{str(report_id)}.zip")
        await self._compression.unarchive(
            data=data, out_path=str(report_id), type="zip"
        )

    async def delete_project(self, report_id: str) -> None:
        if await self._storage.exists(f"{report_id}"):
            await self._storage.delete(f"{report_id}")

        await self._storage.delete(f"{report_id}.zip")
