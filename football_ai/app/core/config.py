from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "dev"
    database_url: str
    espn_base_url: str = "https://site.api.espn.com/apis/site/v2/sports"
    espn_cdn_base_url: str = "https://cdn.espn.com/core"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
