from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_db: str = "langmatinitje"
    postgres_user: str = "creole"
    postgres_password: str = "changeme"
    postgres_host: str = "db"
    postgres_port: int = 5432

    api_key: str = "changeme"
    api_port: int = 8000

    model_config = SettingsConfigDict(
        # Try multiple locations: Docker WORKDIR /app, running from api/, from groupe_scp5/
        env_file=("../../.env", "../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
