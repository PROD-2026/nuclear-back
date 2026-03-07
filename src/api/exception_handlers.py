from typing import Any, Callable

from litestar import Request, Response
from litestar.exceptions import ValidationException
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from src.domain.exceptions import (
    EntityNotFoundError,
)


def validation_error_handler(
    request: Request, exc: ValidationException | ValueError
) -> Response:
    return Response(
        content={"status_code": HTTP_400_BAD_REQUEST, "detail": str(exc)},
        status_code=HTTP_400_BAD_REQUEST,
    )


def not_found_handler(request: Request, exc: EntityNotFoundError) -> Response:
    return Response(
        content={"status_code": HTTP_404_NOT_FOUND, "detail": str(exc)},
        status_code=HTTP_404_NOT_FOUND,
    )


def make_exception_handlers() -> dict[
    type[Exception], Callable[[Request, Any], Response]
]:
    return {
        ValidationException: validation_error_handler,
        EntityNotFoundError: not_found_handler,
    }
