import os
from typing import Final

from pydantic import BaseSettings, PostgresDsn


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
    TIMEOUT: Final[int] = 120

    # Database connection parameters
    POSTGRES_DNS: Final[PostgresDsn]

    # Tesseract-OCR path
    TESSDATA_PREFIX: Final[str]

    class Config:
        env_file = ".env"


class prod_configs(dev_configs):
    pass


class test_configs(dev_configs):
    pass


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
