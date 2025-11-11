from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # Database Configuration
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: str
    secret_key: str 
    access_token_expire_minutes: int
    frontend_url: str
    admin1_email: str = Field(..., env="ADMIN1_EMAIL")
    admin1_password: str = Field(..., env="ADMIN1_PASSWORD")

    admin2_email: str = Field(..., env="ADMIN2_EMAIL")
    admin2_password: str = Field(..., env="ADMIN2_PASSWORD")


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    secret_key: str = Field(str , env="secret_key")
    access_token_expire_minutes: int = Field(60 , env="ACCESS_TOKEN_EXPIRE_MINUTES")

    frontend_url: str = Field("http://127.0.0.1:5500", env="FRONTEND_URL")

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

settings = Settings()
