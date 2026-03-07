from punq import Container

from src.application.services.report import ReportService
from src.application.services.uploads import UploadsService
from src.config import AppConfig
from src.infrastructure.adapters.compression import FSCompressionProvider
from src.infrastructure.adapters.db import IDBProvider, MongoDBProvider
from src.infrastructure.adapters.storage import FSStorageProvider
from src.infrastructure.repositories.report import ReportRepository
from src.ports.compression import ICompressionProvider
from src.ports.report_repo import IReportRepository
from src.ports.storage import IStorageProvider


def build_container() -> Container:
    container = Container()
    config = AppConfig()  # type: ignore

    container.register(AppConfig, instance=config)

    # Providers
    container.register(
        IStorageProvider, instance=FSStorageProvider(base_path=config.uploads_base_path)
    )
    container.register(
        ICompressionProvider,
        instance=FSCompressionProvider(base_path=config.projects_base_path),
    )
    container.register(
        IDBProvider,
        instance=MongoDBProvider(
            connection_uri=config.mongo_uri, database=config.database_name
        ),
    )

    # Repositories
    container.register(
        IReportRepository,
        instance=ReportRepository(db_provider=container.resolve(IDBProvider)),
    )

    # Services
    container.register(
        UploadsService,
        factory=lambda: UploadsService(
            storage_provider=container.resolve(IStorageProvider),
            compression_provider=container.resolve(ICompressionProvider),
        ),
    )
    container.register(
        ReportService,
        factory=lambda: ReportService(repository=container.resolve(IReportRepository)),
    )

    return container
