from punq import Container

from src.application.services.recommendations import RecommendationsService
from src.application.services.report import ReportService
from src.application.services.scanner import ScannerService
from src.application.services.uploads import UploadsService
from src.infrastructure.adapters.compression import FSCompressionProvider
from src.infrastructure.adapters.config import SECRET_PATTERNS, Settings
from src.infrastructure.adapters.db import IDBProvider, MongoDBProvider
from src.infrastructure.adapters.ml import MLProvider
from src.infrastructure.adapters.storage import FSStorageProvider
from src.infrastructure.repositories.report import ReportRepository
from src.ports.compression import ICompressionProvider
from src.ports.ml import IMLProvider
from src.ports.report_repo import IReportRepository
from src.ports.storage import IStorageProvider


def build_container() -> Container:
    container = Container()
    config = Settings()  # type: ignore

    container.register(Settings, instance=config)

    # Providers
    container.register(
        IStorageProvider,
        instance=FSStorageProvider(
            base_path=config.uploads_base_path,
            projects_base_path=config.projects_base_path,
        ),
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
    container.register(
        IMLProvider, instance=MLProvider(base_url=config.predictions_base_url)
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
    container.register(
        ScannerService,
        factory=lambda: ScannerService(
            storage_provider=container.resolve(IStorageProvider),
            compression_provider=container.resolve(ICompressionProvider),
            ml_provider=container.resolve(IMLProvider),
            secrets_patterns=SECRET_PATTERNS,
        ),
    )
    container.register(
        RecommendationsService,
        factory=lambda: RecommendationsService(
            ml_provider=container.resolve(IMLProvider)
        ),
    )

    return container
