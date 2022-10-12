import os
from typing import Any, Final

from pydantic import BaseSettings


class base_config(BaseSettings):
    SECRET_KEY: Final[Any]
    POSTGRES_HOSTNAME: Final[str]
    POSTGRES_USER: Final[str]
    POSTGRES_PASSWORD: Final[str]
    POSTGRES_PORT: Final[int]
    POSTGRES_DATABASE_NAME: Final[str]

    class Config:
        env_file = ".api_env"


configs = base_config()
