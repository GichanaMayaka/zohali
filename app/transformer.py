import os
from typing import List, NoReturn

import pytesseract
from colorama import Fore, Style
from PIL import Image, ImageEnhance

from config import configs
from patterns import Regexes
from exceptions import ZohaliException


class Transformer:
    """
    Transformer class that extracts text from the images passed as method parameters.
    Extracted text are stored in a .txt file named similarly as the input image.
    """
    # Static initialiser block, sort of... this isn't Java afterall
    print(Fore.GREEN + Style.BRIGHT +
          "[+] Starting Transformer module." + Style.RESET_ALL)
    try:
        print(Fore.LIGHTCYAN_EX +
              "[!] Attempting to create text folder" + Style.RESET_ALL)
        os.mkdir("./image_texts/")

    except FileNotFoundError as e:
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
              "[!] Cannot create text folder. Exiting" + Style.RESET_ALL)
        exit(1)
    except FileExistsError as e:
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
              "[!] Text folder already exists. Continuing" + Style.RESET_ALL)

    @staticmethod
    def transform(image_paths: List[str]) -> List[str]:
        text_paths: list = []

        if type(image_paths) == list and len(image_paths) > 0:
            for image_path in image_paths:
                if image_path.endswith(".png"):
                    img = Image.open(image_path).convert("L")
                    enhancer = ImageEnhance.Brightness(img)
                    image = enhancer.enhance(1.5)
                    sharper = ImageEnhance.Sharpness(image=image)
                    sharped_image = sharper.enhance(2)
                    image_text = pytesseract.image_to_string(
                        sharped_image, lang="swa")

                    path_to_write: str = f"./image_texts/{image_path.split('/')[-1].split('.')[0]}.txt"
                    with open(path_to_write, "w", encoding=configs.ENCODING) as file:
                        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
                              f"[!] Writing text to: {path_to_write}" + Style.RESET_ALL)
                        file.write(image_text)
                        text_paths.append(
                            path_to_write)
        else:
            # TODO: create a custom exceptions class
            raise ZohaliException(
                "No parameter supplied, or wrong parameter type supplied")

        return text_paths

    @staticmethod
    def consumer(text_paths: List[str]) -> NoReturn:

        if type(text_paths) == list and len(text_paths) > 0:
            if Regexes.COUNTY:
                pass
        return


if __name__ == "__main__":
    Transformer.transform("./image_texts/image_1.png")
