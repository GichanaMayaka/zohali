import os
import platform
import sys
from typing import Optional

import pandas as pd
from colorama import Fore, Style

from .authenticators import Authenticator
from .tweetListeners import ListenerBuilder, TweetListener


class Runner:
    def __init__(self, max_id: Optional[int] = None, since_id: Optional[int] = None):
        self.tweet_listener: ListenerBuilder = TweetListener(
            authenticator=Authenticator(), max_id=max_id, since_id=since_id
        )

    def fetcher(self) -> pd.DataFrame:
        """
        fetch tweets and parse them into a pandas dataframe
        """
        tweets: list = self.tweet_listener.fetch_tweets()
        image_paths: list = self.tweet_listener.parse_tweets(tweets=tweets)
        text_paths: list = self.tweet_listener.transform(image_paths=image_paths)
        data: pd.DataFrame = self.tweet_listener.tablify(text_file_paths=text_paths)

        return data

    def build_project_structure(self) -> None:
        """
        Build project's directory structure
        """
        print(Fore.GREEN + Style.BRIGHT + "[+] Building listener..." + Style.RESET_ALL)

        try:
            if platform.platform().startswith("Windows"):
                # TODO: remove in production
                # TODO: Correctly handle path
                os.chdir("D:/Projects/zohali/app")

            elif platform.platform().startswith("Linux"):
                os.chdir("./app")

            print(Fore.LIGHTCYAN_EX + "[!] Attempting to create app folders.")

            os.mkdir("./images/")
            os.mkdir("./image_texts/")
            print(Fore.LIGHTCYAN_EX + "[!] App folders created.")

        except FileNotFoundError:
            print(
                Fore.LIGHTRED_EX
                + "[-] Cannot create application folders. Exiting"
                + Style.RESET_ALL
            )
            sys.exit(-1)

        except FileExistsError:
            print(
                Fore.LIGHTMAGENTA_EX
                + "[!] App folders already exist! Continuing"
                + Style.RESET_ALL
            )

        finally:
            print(Fore.LIGHTMAGENTA_EX + "[!] Starting listener..." + Style.RESET_ALL)


if __name__ == "__main__":
    runner: Runner = Runner()
    runner.build_project_structure()
    runner.fetcher()
