FROM python:3.14-alpine AS base

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_COMPILE_BYTECODE=1
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --no-dev

COPY entrypoint.sh .
COPY entrypoint_worker.sh .
COPY src src

ENTRYPOINT [ "ash", "entrypoint.sh" ]

FROM base AS celery

ENTRYPOINT [ "ash", "entrypoint_worker.sh" ]
