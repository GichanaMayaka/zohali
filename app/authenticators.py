import sys
from abc import ABC, abstractmethod

import tweepy
from colorama import Fore, Style
from confs.config import configs


class AbstractAuthenticator(ABC):
    """
        Authentication Base class
    """

    def __init__(
        self,
        api_key: str = configs.API_KEY,
        api_key_secret: str = configs.API_KEY_SECRET,
        access_token: str = configs.ACCESS_TOKEN,
        access_token_secret: str = configs.ACCESS_TOKEN_SECRET
    ):
        self.status = False
        self.api = None

        self.authenticate(api_key=api_key, api_key_secret=api_key_secret,
                          access_token=access_token, access_token_secret=access_token_secret)

    @abstractmethod
    def authenticate(self, api_key: str, api_key_secret: str, access_token: str, access_token_secret: str) -> None:
        """Handle tweepy authentication"""

    @property
    @abstractmethod
    def authentication_status(self) -> bool:
        """Authentication status property"""

    @abstractmethod
    def get_api(self) -> tweepy.API:
        """Return API object"""


class Authenticator(AbstractAuthenticator):
    def authenticate(
        self,
        api_key: str = configs.API_KEY,
        api_key_secret: str = configs.API_KEY_SECRET,
        access_token: str = configs.ACCESS_TOKEN,
        access_token_secret: str = configs.ACCESS_TOKEN_SECRET
    ) -> None:
        try:
            auth = tweepy.OAuthHandler(api_key, api_key_secret)
            auth.set_access_token(access_token,
                                  access_token_secret)

            self.api = tweepy.API(auth, wait_on_rate_limit=True)

            self.api.verify_credentials()

            print(Fore.LIGHTBLUE_EX + Style.BRIGHT +
                  '[+] Authenticated successfully.' + Style.RESET_ALL
                  )
            self.status = True

        except tweepy.errors.Unauthorized as error:
            raise Exception("Unauthorised credentials") from error

    @property
    def authentication_status(self) -> bool:
        return self.status

    def get_api(self) -> tweepy.API:
        return self.api


if __name__ == "__main__":
    auth: AbstractAuthenticator = Authenticator()
