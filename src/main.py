from contextlib import asynccontextmanager
from typing import AsyncGenerator

from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.logging import LoggingConfig
from litestar.openapi import OpenAPIConfig

OPENAPI_CONFIG = OpenAPIConfig(title="LeakSniffer API", version="1.0.0")
LOGGING_CONFIG = LoggingConfig(log_exceptions="debug", disable_stack_trace={404})
CORS_CONFIG = CORSConfig(allow_origins=["*"])


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncGenerator[None, None]:
    yield


app = Litestar(
    openapi_config=OPENAPI_CONFIG,
    logging_config=LOGGING_CONFIG,
    cors_config=CORS_CONFIG,
    route_handlers=[],
    # exception_handlers=make_exception_handlers(),  # type: ignore
    lifespan=[lifespan],
)
