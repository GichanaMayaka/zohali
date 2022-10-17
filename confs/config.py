import os
from typing import Final

from pydantic import BaseSettings


class dev_configs(BaseSettings):
    ENCODING: Final[str] = "utf-8"
    API_KEY: Final[str]
    API_KEY_SECRET: Final[str]
    BEARER_TOKEN: Final[str]
    ACCESS_TOKEN: Final[str]
    ACCESS_TOKEN_SECRET: Final[str]
    SCREEN_NAME: Final[str] = "KenyaPower_Care"
    TWEET_MODE: Final[str] = "extended"
    TWEETS_COUNT: Final[int] = 900
    EXCLUDE_REPLIES: Final[bool] = True
    INCLUDE_RETWEETS: Final[bool] = False
    TIMEOUT: Final[int] = 120  # twitter api timeout in minutes

    # Database connection parameters
    POSTGRES_HOSTNAME: Final[str]
    POSTGRES_USER: Final[str]
    POSTGRES_PASSWORD: Final[str]
    POSTGRES_PORT: Final[int]
    POSTGRES_DATABASE_NAME: Final[str]

    class Config:
        env_file = ".env"


class prod_configs(dev_configs):
    pass

    class Config:
        env_file = ".env"


class test_configs(dev_configs):
    pass

    class Config:
        env_file = ".env"

class ConfigFactory:
    """Inject configuration according to environment at runtime"""

    def factory(self):
        env = os.environ.get("ENV", "development")

        configs = dev_configs()
        testing = test_configs()
        production = prod_configs()

        if env == "development":
            return configs
        if env == "testing":
            return testing
        if env == "production":
            return production


configs = ConfigFactory().factory()
