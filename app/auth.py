import os
from typing import Any, Literal, Union

import pandas as pd
import tweepy
from colorama import Fore, Style


class Authenticator:
    """
    Twitter API Authentication handler for Zohali
    """
    # TODO: Move keys variable to environment variables...
    __status: bool = False

    # Static initialisers
    print(Fore.GREEN + Style.BRIGHT +
          "[+] Initialising Zohali..." + Style.RESET_ALL)
    try:
        os.chdir("D:/Projects/zohali/app")
        os.mkdir("./images/")

    except FileNotFoundError as e:
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
              "[!] Cannot create image[s] folders... Exiting" + Style.RESET_ALL)
        exit(1)
    except FileExistsError as e:
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
              "[!] App Image[s] already exist... Continuing" + Style.RESET_ALL)

    @staticmethod
    def authenticate() -> tweepy.API:

        try:
            credentials = pd.read_csv("./keys.csv", sep="|")
            api_key = credentials.loc[0, "API Key"]
            api_secrets = credentials.loc[0, "API Key Secret"]
            access_token = credentials.loc[0, "Access Token"]
            access_secret = credentials.loc[0, "Access Token Secret"]
        except FileNotFoundError as error:
            print(Fore.RED + Style.DIM +
                  "[-] keys not found. exiting..." + Style.RESET_ALL)
            exit(1)
        except KeyError as error:
            print(error)

        except Exception as error:
            print(Fore.LIGHTMAGENTA_EX + Style.DIM +
                  f"[!] Exception Encountered in authenticate(): + {error}" + Style.RESET_ALL)

        # Authenticate to Twitter
        try:
            auth = tweepy.OAuthHandler(api_key, api_secrets)
            auth.set_access_token(access_token, access_secret)

            api = tweepy.API(auth)

            api.verify_credentials()
            print(Fore.CYAN + Style.BRIGHT +
                  '[+] Authenticated successfully...' + Style.RESET_ALL)
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
