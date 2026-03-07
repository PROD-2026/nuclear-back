from dataclasses import asdict

from src.domain.aggregates.report import Report
from src.ports.db import IDBProvider
from src.ports.report_repo import IReportRepository


class ReportRepository(IReportRepository):
    def __init__(
        self, db_provider: IDBProvider, collection_name: str = "reports"
    ) -> None:
        self._db = db_provider

        self.collection_name = collection_name

    async def get(self, **kwargs) -> Report | None:
        doc = await self._db.get(collection_name=self.collection_name, **kwargs)
        if not doc:
            return

        return Report(**doc)

    async def list(
        self,
        limit: int = 0,
        offset: int = 0,
        orderings: list[str] | None = None,
        **kwargs,
    ) -> list[Report]:
        docs = await self._db.list(
            collection_name=self.collection_name,
            limit=limit,
            offset=offset,
            orderings=orderings,
            **kwargs,
        )

        return [Report(**doc) for doc in docs]

    async def save(self, entity: Report) -> None:
        if not await self._db.get(
            collection_name=self.collection_name, id=str(entity.id)
        ):
            await self._db.insert(
                collection_name=self.collection_name, data=asdict(entity)
            )
            return

        await self._db.update(
            collection_name=self.collection_name, id=entity.id, data=asdict(entity)
        )
