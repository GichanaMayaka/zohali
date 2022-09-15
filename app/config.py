from typing import Final
from pydantic import BaseSettings


class base_configs(BaseSettings):
    ENCODING: Final[str]
    API_KEY: Final[str]
    API_KEY_SECRET: Final[str]
    BEARER_TOKEN: Final[str]
    ACCESS_TOKEN: Final[str]
    ACCESS_TOKEN_SECRET: Final[str]

    class Config:
        env_file = ".env"


class prod_configs(base_configs):
    pass


class test_configs(base_configs):
    pass


configs = base_configs()
production = prod_configs()
test = test_configs()
