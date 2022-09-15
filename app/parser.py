from typing import Any, List, NoReturn

import requests
from colorama import Fore, Style

from auth import Authenticator
from transformer import Transformer
from config import configs


class Parser:
    """
    Parser class that sends a request to the Twitter endpoint: v1/tweets/timelines/api-reference/get-statuses-user_timeline
    fetching the timeline tweets for the respective user- KenyaPower_Care - in the default case. 

    The response[s] are passed through a parsing method: parse_tweets() that extracts the image link[s], and download the images to disk.
    Functionalities handled herein include fetching, searching, and parsing.
    """
    # TODO: Convert print statements into logging statements...
    _max_id: float = 0
    _encoding: str = configs.encoding

    @staticmethod
    def fetch_tweets() -> Any:
        api = Authenticator.authenticate()

        if Authenticator.authentication_status:
            tweets = api.user_timeline(max_id=Parser._max_id, screen_name="KenyaPower_Care", tweet_mode="extended",
                                       count=900, exclude_replies=True, include_rts=False)

        return tweets

    @staticmethod
    def parse_tweets() -> List[str]:

        tweets: Any = Parser.fetch_tweets()
        image_paths = []

        print(Fore.LIGHTMAGENTA_EX +
              Style.BRIGHT + "[!] Match found...")

        for tweet in tweets:
            if ("scheduled" in tweet.full_text or "planned" in tweet.full_text or "maintenance" in tweet.full_text or "interruption" in tweet.full_text) and tweet.entities.get("media"):
                for media in tweet.entities.get("media"):
                    image_data = requests.get(media.get("media_url")).content

                    with open(f"./images/image_{tweet.created_at.strftime('%Y%m%d_%H%M%S')}.png", "wb") as img:
                        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
                              f"[!] Writing image to ./images/image_{tweet.created_at.strftime('%Y%m%d_%H%M%S')}.png to disk..." + Style.RESET_ALL)
                        image_paths.append(
                            f"./images/image_{tweet.created_at.strftime('%Y%m%d_%H%M%S')}.png")
                        img.write(image_data)

        return image_paths

    @staticmethod
    def run(id: float = None) -> NoReturn:
        """Parser class entry point"""
        Parser._max_id: float = id
        Transformer.transform(Parser.parse_tweets())


if __name__ == "__main__":
    # Parser.run(id=None)
    Authenticator.authenticate()
