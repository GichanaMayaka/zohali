from app.parser import Parser
from app.transformer import Transformer
from app.utils import Functions


def serve():
    tweets = Parser.fetch_tweets()
    buff = Transformer.transform(Parser.parse_tweets(tweets=tweets))
    return Transformer.tablify(buff)


data = serve()
Functions.save(df=data)
