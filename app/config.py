from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    yandex_api_key: str
    yandex_folder_id: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
