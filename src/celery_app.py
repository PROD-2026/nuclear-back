from celery import Celery

# TODO: Подсасывать из настроек uri подключения к брокеру и бекенду, настройки через DI надо доставать думаю
app = Celery(
    "nuclear-back",
    broker="test",
    backend="test",
)
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
app.autodiscover_tasks(["src.worker"])
