from celery import Celery

from src.infrastructure.adapters.config import Settings
from src.infrastructure.container import build_container

# TODO: Подсасывать из настроек uri подключения к брокеру и бекенду, настройки через DI надо доставать думаю
CONTAINER = build_container()

app = Celery(
    "nuclear-back",
    broker=CONTAINER.resolve(Settings).celery_broker_uri,
    backend=CONTAINER.resolve(Settings).celery_result_backend,
)
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
app.autodiscover_tasks(["src.worker"])
