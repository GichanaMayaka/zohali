import time
import pandas as pd

from app.config import configs
from app.parser import Parser
from app.transformer import Transformer
from app.utils import Functions


def serve() -> pd.DataFrame:
    data = Transformer.transform(
        Parser.run(max_id=None)
    )
    
    return Transformer.tablify(data)


if __name__ == "__main__":
    while True:
        data = serve()
        Functions.save(df=data)
        time.sleep(configs.TIMEOUT)
