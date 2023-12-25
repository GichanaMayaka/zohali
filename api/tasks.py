import asyncio

import pandas as pd
from app import utils
from app.runner import Runner
from confs.config import configs

from .database import engine


class BackgroundListener:
    """
    Run the task that fetches and parses tweets in the background asynchronously
    """

    def __init__(self, save_to_database: bool = False):
        self.save_to_database = save_to_database
        self.runner = Runner()

    def get_tweets(self) -> pd.DataFrame:
        return self.runner.fetcher()

    async def run_listener(self):
        self.runner.build_project_structure()

        while True:
            data = self.get_tweets()
            if self.save_to_database:
                utils.save(data=data, connection_engine=engine)
            await asyncio.sleep(configs.TIMEOUT)


if __name__ == "__main__":
    BackgroundListener()
