"""App settings.

Values are read from environment variables or the .env file,
so secrets (passwords, API keys) never live inside the code.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "SupportPilot"
    # Read from DATABASE_URL in .env (names are matched case-insensitively)
    database_url: str = "postgresql://postgres:postgres@localhost:5432/supportpilot"


# One shared settings object the rest of the app imports
settings = Settings()
