from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from fastapi.security import OAuth2PasswordBearer


class Settings(BaseSettings):
    # ========= JWT / SECURITY =========
    SECRET_KEY: str = "your-secret"
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # OAuth2 scheme
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
        tokenUrl="/api/auth/token"
    )

    # ========= ADMIN ACCOUNTS =========
    admin1_email: str = Field(..., env="ADMIN1_EMAIL")
    admin1_password: str = Field(..., env="ADMIN1_PASSWORD")
    admin2_email: str = Field(..., env="ADMIN2_EMAIL")
    admin2_password: str = Field(..., env="ADMIN2_PASSWORD")

    # ========= DATABASE ==========
    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., env="POSTGRES_DB")
    postgres_host: str = Field(..., env="POSTGRES_HOST")
    postgres_port: str = Field(..., env="POSTGRES_PORT")

    # ========= FRONTEND ==========
    FRONTEND_URL: str = Field("http://192.168.1.7:8000", env="FRONTEND_URL")

    # Load from .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Computed property
    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
