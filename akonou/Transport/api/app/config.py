import os

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "RTG Grand API MVP"
    api_prefix: str = "/api/v1"
    agent_token: str = "agent-secret"
    eta_default_kmh: float = 22.0
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./rtg.db",
    )


settings = Settings()
