from typing import Any, List, Optional

import os
import sys
import time
import requests
from colorama import Fore, Style

from .auth import Authenticator
from .transformer import Transformer
from .config import configs
from .exceptions import ZohaliException


class Parser:
    """
    Parser class that sends a request to the Twitter endpoint: v1/tweets/timelines/api-reference/get-statuses-user_timeline
    fetching the timeline tweets for the respective user- KenyaPower_Care - in the default case. 

    The response[s] are passed through a parsing method: parse_tweets() that extracts the image link[s], and download the images to disk.
    Functionalities handled herein include fetching, searching, and parsing.
    """
    # TODO: Convert print statements into logging statements...
    __max_id: float = None
    __encoding: str = configs.ENCODING

    # Authentication handlers
    authenticator = Authenticator()
    api = authenticator.authenticate()

    @classmethod
    def fetch_tweets(cls, id: Optional[float] = None) -> Any:

        if Parser.authenticator.authentication_status:
            tweets: list = Parser.api.user_timeline(max_id=id, screen_name=configs.SCREEN_NAME, tweet_mode=configs.TWEET_MODE,
                                                    count=configs.TWEETS_COUNT, exclude_replies=configs.EXCLUDE_REPLIES, include_rts=configs.INCLUDE_RETWEETS)

        else:
            # TODO: add a handler
            pass
        return tweets

    @classmethod
    def parse_tweets(cls, tweets: Any) -> List[str]:

        image_paths: list = []
        # max_tweet_ids: list = []

        for tweet in tweets:
            if ("scheduled" in tweet.full_text or "planned" in tweet.full_text or "maintenance" in tweet.full_text or "interruption" in tweet.full_text) and tweet.entities.get("media"):
                print(Fore.LIGHTBLUE_EX +
                      "[!] Match found..." + Style.RESET_ALL)
                # max_tweet_ids.append(tweet.id)
                for media in tweet.entities.get("media"):
                    image_data: bytes = requests.get(
                        media.get("media_url"), timeout=30
                    ).content

                    # TODO: Add a random salt to image
                    path_to_write = f"./images/image_{tweet.created_at.strftime('%Y%m%d_%H%M%S')}_{tweet.id}.png"
                    with open(path_to_write, "wb") as img:
                        os.chmod(path_to_write, 0o0755)
                        print(Fore.LIGHTBLUE_EX +
                              f"[!] Writing image to {path_to_write}" + Style.RESET_ALL)
                        img.write(image_data)
                        image_paths.append(
                            path_to_write
                        )

        return image_paths

    @classmethod
    def run(cls, id: Optional[float] = None) -> None:
        """Parser class entry point"""
        # Parser.__max_id: float = id

        # try:
        #     tweets = Parser.fetch_tweets()
        #     Transformer.transform(Parser.parse_tweets(tweets=tweets))

        # except ZohaliException:
        #     print(Fore.LIGHTMAGENTA_EX +
        #           "[-] Wrong parameter to transform method" + Style.RESET_ALL)
        #     exit(-1)
        pass

if __name__ == "__main__":
    while True:

        try:
            time.sleep(configs.TIMEOUT)
            Parser.run(id=None)

        except KeyboardInterrupt:
            print(Fore.LIGHTMAGENTA_EX + "[-] Closing." + Style.RESET_ALL)
            sys.exit(-1)
