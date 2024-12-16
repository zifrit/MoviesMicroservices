from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

AUTH_BASE_DIR = Path(__file__).parent.parent.parent


class DBSettings(BaseSettings):
    AUTH_DB_HOST: str = "localhost"
    AUTH_DB_PORT: int = 5432
    AUTH_DB_USER: str = "postgres"
    AUTH_DB_PASS: str = "postgres"
    AUTH_DB_NAME: str = "postgres"

    @property
    def auth_async_database_url(self):
        return f"postgresql+asyncpg://{self.AUTH_DB_USER}:{self.AUTH_DB_PASS}@{self.AUTH_DB_HOST}:{self.AUTH_DB_PORT}/{self.AUTH_DB_NAME}"


class JWTSettings(BaseSettings):
    AUTH_PRIVATE_KEY_FILE: str
    AUTH_PUBLIC_KEY_FILE: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    @property
    def jwt_private_key(self) -> Path:
        return AUTH_BASE_DIR / "src/core/certs" / self.AUTH_PRIVATE_KEY_FILE

    @property
    def jwt_public_key(self) -> Path:
        return AUTH_BASE_DIR / "src/core/certs" / self.AUTH_PUBLIC_KEY_FILE


class RedisSettings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


class Settings(BaseSettings):
    PROJECT_TITLE: str = "auth"
    db_settings: DBSettings = DBSettings()
    jwt_settings: JWTSettings = JWTSettings()
    redis_settings: RedisSettings = RedisSettings()


settings = Settings()
