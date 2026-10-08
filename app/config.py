from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    database_echo: bool = False

    redis_url: str = "redis://localhost:6379/0"
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672//"

    mongo_url: str = "mongodb://localhost:27017"
    mongo_database_name: str = "delivery_service"

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection_name: str = "delivery_knowledge"

    cbr_url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
    http_timeout_seconds: float = 10.0

    session_ttl_seconds: int = 60 * 60 * 24
    exchange_rate_cache_ttl_seconds: int = 300

    yandex_api_key: str
    yandex_folder_id: str
    yandex_api_base_url: str = "https://ai.api.cloud.yandex.net/v1"
    yandex_model_name: str = "yandexgpt/latest"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
