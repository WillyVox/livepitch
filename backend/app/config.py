"""
Central configuration, loaded from environment variables / .env file.
Never hardcode API keys — always load them from here.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- Live score data provider -------------------------------------
    # Provider used by app/livescore_client.py. "api_football" targets
    # https://www.api-football.com (also sold on RapidAPI as
    # "API-FOOTBALL"). Swap to another adapter if you buy a different
    # provider (e.g. LiveScore API, SportMonks, Sportradar).
    LIVESCORE_PROVIDER: str = "api_football"

    API_FOOTBALL_KEY: str = ""
    API_FOOTBALL_BASE_URL: str = "https://v3.football.api-sports.io"

    # How often to poll the provider for live fixtures, in seconds.
    # 15-30s is typical for a paid "live" tier; check your plan's rate limit.
    POLL_INTERVAL_SECONDS: int = 20

    # --- Social auto-posting -------------------------------------------
    ENABLE_SOCIAL_POSTING: bool = False

    TWITTER_API_KEY: str = ""
    TWITTER_API_SECRET: str = ""
    TWITTER_ACCESS_TOKEN: str = ""
    TWITTER_ACCESS_SECRET: str = ""

    FACEBOOK_PAGE_ID: str = ""
    FACEBOOK_PAGE_ACCESS_TOKEN: str = ""

    # TikTok has no public "text status" endpoint — see social_poster.py
    TIKTOK_ACCESS_TOKEN: str = ""

    # --- App -------------------------------------------------------------
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    # --- Data Mode -------------------------------------------------------
    # When true, get_client() returns MockClient instead of hitting the
    # real API — lets you build/demo the whole app without an API key
    # or burning your provider's rate limit. Flip to false once you're
    # ready to go live.
    USE_MOCK_DATA: bool = True

    # --- Redis -----------------------------------------------------------
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


settings = Settings()
