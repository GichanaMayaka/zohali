import os
import platform
from typing import Literal, Union

import tweepy
from colorama import Fore, Style

from .config import configs


class Authenticator:
    """
    Twitter API Authentication handler for Zohali
    """
    __status: bool = False

    # Static initialisers
    print("\n" + Fore.GREEN + Style.BRIGHT +
          "[+] Initialising Zohali..." + Style.RESET_ALL)
    try:
        if platform.platform().startswith("Windows"):
            os.chdir("D:/Projects/zohali/app")

        elif platform.platform().startswith("Linux"):
            os.chdir("/zohali/app")

        print(Fore.LIGHTCYAN_EX +
              "[!] Attempting to create image[s] folder.")
        os.mkdir("./images/")
        print(Fore.LIGHTCYAN_EX + "[!] Created.")

    except FileNotFoundError as e:
        print(Fore.LIGHTRED_EX + Style.BRIGHT +
              "[-] Cannot create image[s] folders. Exiting" + Style.RESET_ALL)
        exit(1)

    except FileExistsError as e:
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
              "[!] App Image[s] folder already exists! Continuing" + Style.RESET_ALL)

    def authenticate(self) -> tweepy.API:
        try:
            auth = tweepy.OAuthHandler(configs.API_KEY, configs.API_KEY_SECRET)
            auth.set_access_token(configs.ACCESS_TOKEN,
                                  configs.ACCESS_TOKEN_SECRET)

            api = tweepy.API(auth, wait_on_rate_limit=True)

            api.verify_credentials()

            print(Fore.LIGHTBLUE_EX + Style.BRIGHT +
                  '[+] Authenticated successfully.' + Style.RESET_ALL)
            Authenticator.__status = True
            return api

        except Exception as e:
            print(Fore.RED + Style.DIM +
                  f'[-] Authentication failed with exception:\n\t {e}...' + Fore.RED + Style.DIM + "\nexiting" + Style.RESET_ALL)

    @property
    def authentication_status(self) -> Union[Literal[True], Literal[False]]:
        return Authenticator.__status


if __name__ == "__main__":
    Authenticator().authenticate()
