from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # --- MongoDB ---
    mongo_uri: str
    database_name: str
    mongo_server_selection_timeout_ms: int = 8000
    mongo_connect_timeout_ms: int = 10000
    mongo_socket_timeout_ms: int = 20000
    # Atlas (especially free/shared tiers) silently drops idle sockets.
    # If pymongo tries to reuse one after Atlas has killed it, you get
    # "SSL: DECRYPTION_FAILED_OR_BAD_RECORD_MAC" / AutoReconnect.
    # Recycling idle connections before Atlas does avoids that.
    mongo_max_idle_time_ms: int = 45000

    # --- NVD sync ---
    nvd_results_per_page: int = 1000
    nvd_sync_days: int = 7
    nvd_api_key: str = "8702e60f-233d-4ad2-82ef-b0f26bec551c"

    # --- HTTP ---
    http_timeout: int = 20

    # --- GitHub ---
    github_token: str = ""
    github_cache_ttl_hours: int = 24

    # --- CORS ---
    # Comma separated list, e.g. "http://localhost:3000,https://app.example.com"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # --- Logging ---
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip() for origin in self.cors_origins.split(",") if origin.strip()
        ]


settings = Settings()
