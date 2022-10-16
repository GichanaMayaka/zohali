import sys
import time
from typing import Any, List, Optional

import requests
from colorama import Fore, Style

from .auth import Authenticator
from .config import configs


class Parser:
    """
    Parser class that sends a request to the Twitter endpoint: v1/tweets/timelines/api-reference/get-statuses-user_timeline
    fetching the timeline tweets for the respective user- KenyaPower_Care - in the default case. 

    The response[s] are passed through a parsing method: parse_tweets() that extracts the image link[s], and download the images to disk.
    Functionalities handled herein include fetching, searching, and parsing.
    """
    # TODO: Convert print statements into logging statements...
    _max_id: Optional[float] = None
    _since_id: Optional[float] = None
    _encoding: str = configs.ENCODING

    # Authentication handlers
    authenticator = Authenticator()
    api = authenticator.authenticate()

    @classmethod
    def fetch_tweets(cls, max_id: Optional[float] = None, since_id: Optional[float] = None) -> Optional[list[Any]]:

        Parser._max_id = max_id
        Parser._since_id = since_id

        if Parser.authenticator.authentication_status:
            tweets: list[Any] = Parser.api.user_timeline(max_id=max_id, since_id=since_id, screen_name=configs.SCREEN_NAME, tweet_mode=configs.TWEET_MODE,
                                                         count=configs.TWEETS_COUNT, exclude_replies=configs.EXCLUDE_REPLIES, include_rts=configs.INCLUDE_RETWEETS)

            if len(tweets) > 0:
                Parser._since_id = max((tweet.id for tweet in tweets))

        return tweets

    @classmethod
    def parse_tweets(cls, tweets: list[Any]) -> List[str]:

        image_paths: list[str] = []

        for tweet in tweets:
            if ("scheduled" in tweet.full_text or "planned" in tweet.full_text or "maintenance" in tweet.full_text or "interruption" in tweet.full_text) and tweet.entities.get("media"):
                print(Fore.LIGHTBLUE_EX +
                      "[!] Match found..." + Style.RESET_ALL)
                for media in tweet.entities.get("media"):
                    image_data: bytes = requests.get(
                        media.get("media_url"), timeout=30
                    ).content

                    # TODO: Add a random salt to image
                    path_to_write = f"./images/image_{tweet.created_at.strftime('%Y%m%d_%H%M%S')}_{tweet.id}.png"
                    with open(path_to_write, "wb") as img:
                        print(Fore.LIGHTBLUE_EX +
                              f"[!] Writing image to {path_to_write}" + Style.RESET_ALL)
                        img.write(image_data)
                        image_paths.append(
                            path_to_write
                        )

        return image_paths

    @classmethod
    def run(cls, max_id: Optional[float] = None) -> List[str]:
        """Parser class entry point and wrapper around fetching tweet and extracting information"""

        tweets = Parser.fetch_tweets(max_id=max_id, since_id=Parser._since_id)
        tweet_paths = Parser.parse_tweets(tweets=tweets)

        return tweet_paths


if __name__ == "__main__":
    while True:

        try:
            time.sleep(configs.TIMEOUT)
            Parser.run(max_id=None)

        except KeyboardInterrupt:
            print(Fore.LIGHTMAGENTA_EX + "[-] Closing." + Style.RESET_ALL)
            sys.exit(-1)
