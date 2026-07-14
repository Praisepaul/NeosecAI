from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    mongo_uri: str
    database_name: str

    nvd_results_per_page: int = 100
    nvd_sync_days: int = 7
    http_timeout: int = 20

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()