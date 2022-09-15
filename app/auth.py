import os
from typing import Literal, Union

import tweepy
from colorama import Fore, Style

from config import configs


class Authenticator:
    """
    Twitter API Authentication handler for Zohali
    """
    __status: bool = False

    # Static initialisers
    print(Fore.GREEN + Style.BRIGHT +
          "[+] Initialising Zohali..." + Style.RESET_ALL)
    try:
        os.chdir("D:/Projects/zohali/app")
        print(Fore.LIGHTCYAN_EX +
              "[!] Attempting to create image[s] folder.")
        os.mkdir("./images/")

    except FileNotFoundError as e:
        print(Fore.LIGHTRED_EX + Style.BRIGHT +
              "[-] Cannot create image[s] folders. Exiting" + Style.RESET_ALL)
        exit(1)
    except FileExistsError as e:
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
              "[!] App Image[s] folder already exists! Continuing" + Style.RESET_ALL)

    @staticmethod
    def authenticate() -> tweepy.API:
        try:
            auth = tweepy.OAuthHandler(configs.API_KEY, configs.API_KEY_SECRET)
            auth.set_access_token(configs.ACCESS_TOKEN,
                                  configs.ACCESS_TOKEN_SECRET)

            api = tweepy.API(auth)

            api.verify_credentials()
            print(Fore.LIGHTBLUE_EX + Style.BRIGHT +
                  '[+] Authenticated successfully.' + Style.RESET_ALL)
            Authenticator.__status = True
            return api

        except Exception as e:
            print(Fore.RED + Style.DIM +
                  f'[-] Authentication failed with exception:\n\t {e}...' + Fore.RED + Style.BRIGHT + "\nexiting" + Style.RESET_ALL)

    @property
    def authentication_status() -> Union[Literal[True], Literal[False]]:
        return Authenticator.__status


if __name__ == "__main__":
    Authenticator.authenticate()
