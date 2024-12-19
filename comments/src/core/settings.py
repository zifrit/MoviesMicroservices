from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

COMMENTS_BASE_DIR = Path(__file__).parent.parent.parent


class DBSettings(BaseSettings):
    COMMENTS_DB_HOST: str = "localhost"
    COMMENTS_DB_PORT: int = 5432
    COMMENTS_DB_USER: str = "postgres"
    COMMENTS_DB_PASS: str = "postgres"
    COMMENTS_DB_NAME: str = "postgres"

    @property
    def auth_async_database_url(self):
        return f"postgresql+asyncpg://{self.COMMENTS_DB_USER}:{self.COMMENTS_DB_PASS}@{self.COMMENTS_DB_HOST}:{self.COMMENTS_DB_PORT}/{self.COMMENTS_DB_NAME}"


class JWTSettings(BaseSettings):
    COMMENTS_PUBLIC_KEY_FILE: str
    ALGORITHM: str

    @property
    def jwt_public_key(self) -> Path:
        return COMMENTS_BASE_DIR / "src/core/certs" / self.COMMENTS_PUBLIC_KEY_FILE


class Settings(BaseSettings):
    PROJECT_TITLE: str = "auth"
    db_settings: DBSettings = DBSettings()
    jwt_settings: JWTSettings = JWTSettings()


settings = Settings()
