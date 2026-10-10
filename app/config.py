"""Централизованные настройки приложения, загружаемые из окружения."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Типизированные настройки приложения."""

    # PostgreSQL
    database_url: str
    database_echo: bool = False

    # Redis
    redis_url: str

    # RabbitMQ
    rabbitmq_url: str

    # MongoDB
    mongo_url: str
    mongo_database_name: str

    # Qdrant
    qdrant_url: str
    qdrant_collection_name: str = "delivery_knowledge"

    # Внешние API
    cbr_url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
    http_timeout_seconds: float = 10.0

    # Кэширование и сессии
    session_ttl_seconds: int = 60 * 60 * 24
    exchange_rate_cache_ttl_seconds: int = 300

    # YandexGPT
    yandex_api_key: str
    yandex_folder_id: str
    yandex_api_base_url: str = "https://ai.api.cloud.yandex.net/v1"
    yandex_model_name: str = "yandexgpt/latest"

    # Логирование
    log_level: str = "INFO"
    log_file: str = "logs/delivery-service.log"
    log_rotation: str = "10 MB"
    log_retention: str = "14 days"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
