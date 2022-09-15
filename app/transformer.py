import os
from typing import List, NoReturn

import pytesseract
from colorama import Fore, Style
from PIL import Image, ImageEnhance

from config import base_configs


class Transformer:
    """
    Transformer class that extracts text from the images passed as method parameters.
    Extracted text are stored in a .txt file named similarly as the input image.
    """
    # Static initialiser block, sort of... this isn't Java afterall
    print(Fore.GREEN + Style.BRIGHT +
          "[+] Starting Transformer module..." + Style.RESET_ALL)
    try:
        os.mkdir("./image_texts/")

    except FileNotFoundError as e:
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
              "[!] Cannot create text folder... Exiting" + Style.RESET_ALL)
        exit(1)
    except FileExistsError as e:
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
              "[!] Text folder already exists... Continuing" + Style.RESET_ALL)

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

                    with open(f"./image_texts/{image_path.split('/')[-1].split('.')[0]}.txt", "w", encoding=base_configs.encoding) as file:
                        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
                              f"[!] Writing text to: ./image_texts/{image_path.split('/')[-1].split('.')[0]}.txt" + Style.RESET_ALL)
                        file.write(image_text)
                        text_paths.append(
                            f"./image_texts/{image_path.split('/')[-1].split('.')[0]}.txt")
        else:
            # TODO: create a custom exceptions class
            pass
        return text_paths

    @staticmethod
    def consume(text_paths: List[str]) -> NoReturn:
        return
