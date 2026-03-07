from contextlib import asynccontextmanager
from typing import AsyncGenerator

from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.logging import LoggingConfig
from litestar.openapi import OpenAPIConfig

from src.api.exception_handlers import make_exception_handlers
from src.api.routers import routers
from src.infrastructure.adapters.config import Settings
from src.infrastructure.container import build_container
from src.ports.db import IDBProvider

OPENAPI_CONFIG = OpenAPIConfig(title="LeakSniffer API", version="1.0.0")
LOGGING_CONFIG = LoggingConfig(log_exceptions="debug", disable_stack_trace={404})
CORS_CONFIG = CORSConfig(allow_origins=["*"])

CONTAINER = build_container()


@asynccontextmanager
async def lifespan(_: Litestar) -> AsyncGenerator[None, None]:
    container = app.state.container
    db: IDBProvider = container.resolve(IDBProvider)

    await db.connect()
    yield
    await db.close()


app = Litestar(
    openapi_config=OPENAPI_CONFIG,
    logging_config=LOGGING_CONFIG,
    cors_config=CORS_CONFIG,
    debug=CONTAINER.resolve(Settings).debug,
    dependencies={"container": lambda: CONTAINER},
    route_handlers=[routers],
    exception_handlers=make_exception_handlers(),  # type: ignore
    lifespan=[lifespan],
)

app.state.container = CONTAINER
