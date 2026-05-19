from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Random Data Tools People"
    app_debug: bool = False

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/people"

    random_data_api_url: str = "https://api.randomdatatools.ru/"
    initial_load_count: int = 1000
    skip_initial_load: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    @property
    def debug(self) -> bool:
        return self.app_debug


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
