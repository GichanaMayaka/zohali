import os
import sys
from typing import List

import pandas as pd
import pytesseract
from colorama import Fore, Style

sys.path.append(".")

from confs.config import configs
from .utils import Functions


class Transformer:
    """
    Transformer class that extracts text from the images passed as method parameters.
    Extracted text are stored in a .txt file named similarly as the input image.
    """
    try:
        base_rel_path = "./image_texts/"
        os.mkdir(base_rel_path)

    except FileNotFoundError as e:
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
              "[!] Cannot create text folder. Exiting" + Style.RESET_ALL)
        sys.exit(-1)
    except FileExistsError as e:
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
              "[!] Text folder already exists. Continuing" + Style.RESET_ALL)

    @classmethod
    def transform(cls, image_paths: List[str]) -> List[str]:

        text_paths: list[str] = []

        if isinstance(image_paths, list) and len(image_paths) > 0:
            for image_path in image_paths:
                if image_path.endswith(".png"):
                    
                    image = Functions.preprocess_image(image_path, brightness=1.5, sharpness=2)
                    image_text = pytesseract.image_to_string(image)

                    path_to_write: str = f"./image_texts/{image_path.split('/')[-1].split('.')[0]}.txt"
                    with open(path_to_write, "w", encoding=configs.ENCODING) as file:
                        print(
                            Fore.LIGHTBLUE_EX + f"[!] Writing text to: {path_to_write}" + Style.RESET_ALL)
                        file.write(image_text)
                        text_paths.append(
                            path_to_write
                        )

        else:
            print("[!] No tweet[s] fetched. Listening...")

        return text_paths

    @classmethod
    def tablify(cls, text_paths: List[str]) -> pd.DataFrame:
        """Build a dataframe from the data parsed from the tweets"""

        columns = ["region", "area", "places", "time", "date",
                   "county", "start_time", "end_time", "file_path",
                   "tweet_id"]

        data = pd.DataFrame(
            columns=columns
        )

        if isinstance(text_paths, list) and len(text_paths) > 0:
            for text_path in text_paths:
                data = pd.concat(
                    objs=[data, Functions.extract_text(text_path)], axis=0
                )

                data["file_path"] = text_path
                data["tweet_id"] = text_path.split("_")[-1].split(".")[0]

        return data


if __name__ == "__main__":
    Transformer.tablify(Transformer.transform([]))
