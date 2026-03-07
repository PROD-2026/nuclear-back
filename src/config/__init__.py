from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    debug: bool = False

    uploads_base_path: str
    projects_base_path: str = "/tmp"

    mongo_uri: str
    database_name: str
