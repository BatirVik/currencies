import os
from pathlib import Path

from pydantic.fields import Field
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator


class Config(BaseSettings):
    DB_URL: PostgresDsn
    LOGS_PATH: Path

    SECRET_KEY: str = Field(min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(15, gt=0)

    @field_validator("LOGS_PATH")
    def absolute_path(cls, value: Path) -> Path:
        return Path(__file__).parent.parent / value


match os.getenv("ENV"):
    case "production":
        dotenv_name = ".env"
    case "test":
        dotenv_name = ".env.test"
    case "development":
        dotenv_name = ".env.dev"
    case _ as env:
        raise ValueError(f"Unknown environment: {env}")


dotenv_path = Path(__file__).parent.parent / "configuration" / dotenv_name
config = Config(_env_file=dotenv_path)  # type: ignore