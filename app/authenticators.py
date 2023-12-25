from abc import ABC, abstractmethod

import tweepy
from colorama import Fore, Style
from confs.config import configs

from .exceptions import FailedToConnectException, InvalidCredentialsException


class AbstractAuthenticator(ABC):
    """
    Authentication Base class
    """

    def __init__(
            self,
            api_key: str = configs.API_KEY,
            api_key_secret: str = configs.API_KEY_SECRET,
            access_token: str = configs.ACCESS_TOKEN,
            access_token_secret: str = configs.ACCESS_TOKEN_SECRET,
    ):
        self.status = False
        self.api = None

        self.authenticate(
            api_key=api_key,
            api_key_secret=api_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

    @abstractmethod
    def authenticate(
            self,
            api_key: str,
            api_key_secret: str,
            access_token: str,
            access_token_secret: str,
    ) -> None:
        """Handle tweepy authentication"""

    @property
    @abstractmethod
    def is_authenticated(self) -> bool:
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
            access_token_secret: str = configs.ACCESS_TOKEN_SECRET,
    ) -> None:
        auth_handler = tweepy.OAuth1UserHandler(
            consumer_key=api_key,
            consumer_secret=api_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

        try:
            self.api = tweepy.API(auth_handler, wait_on_rate_limit=True)

            self.api.verify_credentials()

            print(
                Fore.LIGHTBLUE_EX
                + Style.BRIGHT
                + "[+] Authenticated successfully."
                + Style.RESET_ALL
            )
            self.status = True

        except tweepy.errors.Unauthorized as error:
            raise InvalidCredentialsException(
                "Unauthorised/Invalid credentials"
            ) from error

        except tweepy.errors.TweepyException as error:
            raise FailedToConnectException(
                "Failed to Connect to the server[s]"
            ) from error

        except TypeError as error:
            raise Exception("Not a parser object") from error

    @property
    def is_authenticated(self) -> bool:
        return self.status

    def get_api(self) -> tweepy.API:
        return self.api


if __name__ == "__main__":
    auth: AbstractAuthenticator = Authenticator()
