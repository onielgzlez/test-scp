from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings."""
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    n8n_url: str = "http://localhost:5678"
    app_host: str = "0.0.0.0"
    app_port: int = 7013
    debug: bool = True

    # Selenium settings
    REMOTE_DRIVER_URL: str = "selenium"
    REMOTE_DRIVER_PORT: int = 4444

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Virtual Assistant"

    # Scraping settings
    MAX_BOOKS_TO_SCRAPE: int = 100
    MAX_BOOK_PRICE: float = 20.0
    HN_PAGES_TO_SCRAPE: int = 5

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 