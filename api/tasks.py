import asyncio
import sys

import pandas as pd

sys.path.append(".")
from app import utils
from app.runner import Runner
from confs.config import configs

from .database import engine


class BackgroundListener:
    """
        Run the task that fetches and parses tweets in the background asynchronously
    """

    def __init__(self):
        self.runner = Runner()

    def build_project(self):
        self.runner.build_project_structure()

    def get_tweets(self) -> pd.DataFrame:
        return self.runner.fetcher()

    async def run_listener(self):
        self.build_project()

        while True:
            data = self.get_tweets()
            utils.save(data=data, connection_engine=engine)
            await asyncio.sleep(configs.TIMEOUT)


if __name__ == "__main__":
    BackgroundListener()
