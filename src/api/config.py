from enum import Enum

from pydantic import EmailStr, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = ".env"

class Config(BaseConfig):
    ANALYTICS_DATABASE_URL: str

config: Config = Config()