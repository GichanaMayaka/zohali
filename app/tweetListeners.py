import random
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List, Any

import pandas as pd
import pytesseract
import requests
from colorama import Fore, Style

from confs.config import configs
from . import utils
from .authenticators import AbstractAuthenticator, Authenticator


class ListenerBuilder(ABC):
    """
        Abstract base class defining the listener's contract.
        This class contains methods to authenticate, fetch relevant tweets, parse the tweets,
        transform parsed tweet texts, and convert them into a pandas dataframe for easy manipulation
        downstream.
        Constructor params include the max_id, since_id, and the authentication method to use which has been
        implemented in the Authenticator class
    """

    def __init__(self, authenticator: AbstractAuthenticator, max_id: Optional[int] = None,
                 since_id: Optional[int] = None,
                 ):
        self._max_id = max_id
        self._since_id = since_id
        self._encoding = configs.ENCODING
        self._auther = authenticator
        self._api = self._auther.get_api()
        self._authentication_status = self._auther.authentication_status

    @abstractmethod
    def fetch_tweets(self) -> Optional[List[Any]]:
        """Fetch tweets"""

    @abstractmethod
    def parse_tweets(self, tweets: list[Any]) -> List[str]:
        """Parse tweet images as the target tweets always contain images"""

    @abstractmethod
    def transform(self, image_paths: List[str]) -> List[str]:
        """Consume the text files to generate pattern matches using the predefined patterns from Patterns class"""

    @abstractmethod
    def tablify(self, text_file_paths: List[str]) -> pd.DataFrame:
        """Build a dataframe for manipulation and storage to the database"""


class TweetListener(ListenerBuilder):
    def __init__(self, authenticator: AbstractAuthenticator, max_id: Optional[int] = None,
                 since_id: Optional[int] = None):
        super(TweetListener, self).__init__(max_id=max_id,
                                            since_id=since_id, authenticator=authenticator)

    def fetch_tweets(self) -> Optional[List[Any]]:
        if self._authentication_status:
            tweets: list[Any] = self._api.user_timeline(
                max_id=self._max_id,
                since_id=self._since_id,
                screen_name=configs.SCREEN_NAME,
                tweet_mode=configs.TWEET_MODE,
                count=configs.TWEETS_COUNT,
                exclude_replies=configs.EXCLUDE_REPLIES,
                include_rts=configs.INCLUDE_RETWEETS
            )

            if len(tweets) > 0:
                self._since_id = max((tweet.id for tweet in tweets))

        return tweets

    def parse_tweets(self, tweets: list[Any]) -> List[str]:
        image_paths: list[str] = []

        for tweet in tweets:
            if (
                    "scheduled" in tweet.full_text or "planned" in tweet.full_text or "maintenance" in tweet.full_text or "interruption" in tweet.full_text) \
                    and tweet.entities.get(
                        "media"
            ):
                print(Fore.LIGHTBLUE_EX +
                      f"[!] Match found... @ {datetime.now().strftime('%H:%M:%S')}" + Style.RESET_ALL)

                for media in tweet.extended_entities.get("media"):
                    image_data: bytes = requests.get(
                        media.get("media_url"), timeout=30
                    ).content

                    path_to_write: str = f"./images/image_{tweet.created_at.strftime('%Y%m%d_%H%M%S')}_{random.randint(1, 1000)}_{tweet.id}.png"
                    with open(path_to_write, "wb") as img:
                        print(Fore.LIGHTBLUE_EX +
                              f"[!] Writing image to {path_to_write}" + Style.RESET_ALL)
                        img.write(image_data)
                        image_paths.append(
                            path_to_write
                        )

        return image_paths

    def transform(self, image_paths: List[str]) -> List[str]:
        text_paths: list[str] = []

        if isinstance(image_paths, list) and len(image_paths) > 0:
            for image_path in image_paths:
                if image_path.endswith(".png") or image_path.endswith(".jpg") or image_path.endswith(".jpeg"):
                    image = utils.preprocess_image(
                        image_path, brightness=1.5, sharpness=2)
                    image_text = pytesseract.image_to_string(image)

                    path_to_write: str = f"./image_texts/{image_path.split('/')[-1].split('.')[0]}.txt"
                    with open(path_to_write, "w", encoding=self._encoding) as file:
                        print(
                            Fore.LIGHTBLUE_EX + f"[!] Writing text to: {path_to_write}" + Style.RESET_ALL)
                        file.write(image_text)
                        text_paths.append(
                            path_to_write
                        )

        else:
            print("[!] No tweet[s] fetched. Listening...")

        return text_paths

    def tablify(self, text_file_paths: List[str]) -> pd.DataFrame:
        """Build a dataframe from the data parsed from the tweets"""

        columns = [
            "region", "area", "places", "time", "date",
            "county", "start_time", "end_time", "file_path",
            "tweet_id"
        ]

        data = pd.DataFrame(
            columns=columns
        )

        if isinstance(text_file_paths, list) and len(text_file_paths) > 0:
            for text_file_path in text_file_paths:
                data = pd.concat(
                    objs=[data, utils.extract_text(text_file_path)], axis=0
                )

                data["file_path"] = text_file_path
                data["tweet_id"] = text_file_path.split("_")[-1].split(".")[0]

        return data


if __name__ == "__main__":
    listener: ListenerBuilder = TweetListener(
        Authenticator(), max_id=None, since_id=None)
