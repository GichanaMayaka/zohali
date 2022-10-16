import asyncio
import sys

import pandas as pd

sys.path.append(".")

from app.config import configs
from app.parser import Parser
from app.transformer import Transformer
from app.utils import Functions

from .database import engine


class BackgroundListener:
    """Run the task that fetches and parses tweets in the background asynchonously"""
    def get_tweets(self) -> pd.DataFrame:

        data = Transformer.transform(
            Parser.run(max_id=None)
        )

        return Transformer.tablify(data)

    async def run_listener(self):
        while True:
            data = self.get_tweets()
            Functions.save(df=data, connection_engine=engine)
            await asyncio.sleep(configs.TIMEOUT)


if __name__ == "__main__":
    b = BackgroundListener()
    print(b.run_listener())
