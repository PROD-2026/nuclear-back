from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    debug: bool = False

    uploads_base_path: str
    projects_base_path: str = "/tmp"

    mongo_uri: str
    database_name: str

    celery_broker_uri: str
    celery_result_backend: str
