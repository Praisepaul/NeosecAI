from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    mongo_uri: str

    database_name: str

    nvd_results_per_page: int = 100

    nvd_sync_days: int = 7

settings = Settings()