from typing import Final
from pydantic import BaseSettings


class base_configs(BaseSettings):
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
    TIMEOUT: Final[int] = 15 # twitter api timeout in minutes

    class Config:
        env_file = ".env"


class prod_configs(base_configs):
    pass


class test_configs(base_configs):
    pass


configs = base_configs()
test = test_configs()
production = prod_configs()
