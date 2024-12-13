from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

AUTH_BASE_DIR = Path(__file__).parent.parent.parent


class DBSettings(BaseSettings):
    MOVIES_DB_HOST: str = "localhost"
    MOVIES_DB_PORT: int = 5432
    MOVIES_DB_USER: str = "postgres"
    MOVIES_DB_PASS: str = "postgres"
    MOVIES_DB_NAME: str = "postgres"

    @property
    def auth_async_database_url(self):
        return f"postgresql+asyncpg://{self.MOVIES_DB_USER}:{self.MOVIES_DB_PASS}@{self.MOVIES_DB_HOST}:{self.MOVIES_DB_PORT}/{self.MOVIES_DB_NAME}"


class JWTSettings(BaseSettings):
    MOVIES_PUBLIC_KEY_FILE: str
    ALGORITHM: str

    @property
    def jwt_public_key(self) -> Path:
        return AUTH_BASE_DIR / "src/core/certs" / self.AUTH_PUBLIC_KEY_FILE


class Settings(BaseSettings):
    PROJECT_TITLE: str = "auth"
    db_settings: DBSettings = DBSettings()
    jwt_settings: JWTSettings = JWTSettings()


settings = Settings()
