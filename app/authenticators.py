import sys
from abc import ABC, abstractmethod

import tweepy
from colorama import Fore, Style
from confs.config import configs


class AbstractAuthenticator(ABC):
    def __init__(self):
        self.status = False
        self.api = None

        self.authenticate()

    @abstractmethod
    def authenticate(self) -> tweepy.API:
        """Handle tweepy authentication"""

    @property
    @abstractmethod
    def authentication_status(self) -> bool:
        """Authentication status property"""

    @abstractmethod
    def get_api(self) -> tweepy.API:
        """Return API object"""


class Authenticator(AbstractAuthenticator):
    def __init__(self):
        super(Authenticator, self).__init__()

    def authenticate(self) -> None:
        try:
            auth = tweepy.OAuthHandler(configs.API_KEY, configs.API_KEY_SECRET)
            auth.set_access_token(configs.ACCESS_TOKEN,
                                  configs.ACCESS_TOKEN_SECRET)

            self.api = tweepy.API(auth, wait_on_rate_limit=True)

            self.api.verify_credentials()

            print(Fore.LIGHTBLUE_EX + Style.BRIGHT +
                  '[+] Authenticated successfully.' + Style.RESET_ALL
                  )
            self.status = True

        except TypeError as error:
            print(Fore.RED + Style.DIM +
                  f'[-] Authentication failed with exception:\n\t {error}...' +
                  Fore.RED + Style.DIM + "\nexiting" + Style.RESET_ALL
                  )
            sys.exit(0)

    def authentication_status(self) -> bool:
        return self.status

    def get_api(self) -> tweepy.API:
        return self.api


if __name__ == "__main__":
    auth: AbstractAuthenticator = Authenticator()
