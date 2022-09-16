from re import Pattern
from typing import AnyStr, Final

import regex as re


class Regexes:
    """
    constant Regexes exporting class
    """
    TIME: Final[Pattern[AnyStr]] = re.compile(pattern=r"(?<=time.+?)(\d{1,2}\.\d{2}\s+?(\S)*)(-*\s*|—*\s*)*(\d{1,2}\.\d{2}\s+?(\S)*)", flags=re.IGNORECASE)
    DATE: Final[Pattern[AnyStr]] = re.compile(pattern=r"\d{1,2}\.+?\d{1,2}\.+?\d{2,4}")
    COUNTY: Final[Pattern[AnyStr]] = re.compile(pattern=r"(\w+?\s*?){1}-*?(\w+?\s*?){1}(?=county)", flags=re.IGNORECASE)
    AREAS: Final[Pattern[AnyStr]] = re.compile(pattern=r"(?<=area:*?)\s*?[\w\s\d\|\.,\\\-]+(?=date)", flags=re.IGNORECASE)
    PLACES: Final[Pattern[AnyStr]] = re.compile(pattern=r"(?<=p\.m\.)\s*?[\w\d\s\.\/\':\-]+(,+?[\w\d\s\|\/\':\-$£&]*)+[\.|\n]+?", flags=re.IGNORECASE)
    REGIONS: Final[Pattern[AnyStr]] = re.compile(pattern=r"(\w+\s*\d*){2}\s*?(?=region)", flags=re.IGNORECASE)
