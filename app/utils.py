import sys
from collections import OrderedDict
from typing import Any, Optional

import pandas as pd
from PIL import Image, ImageEnhance

sys.path.append(".")

from confs.config import configs

from .patterns import Patterns

"""
Utility functions applied to the dataframe for various actions
including cleaning, extracting text, imputing null rows, writing to database, 
and more. This class is not meant to be subclassed
"""


def extract_text(path: str) -> pd.DataFrame:
    """
        Actual workhorse method. Matches patterns, and extracts the matched information into a dataframe
    """

    with open(path, "r", encoding=configs.ENCODING) as f:
        string = " ".join([line.rstrip() for line in f.readlines()])
        string = string.lower().replace(
            "mr.", "Mr").replace(
            "st.", "St").replace(
            "mt.", "Mt"
        )

    info = {}

    region, county, place, date, time, area = match_patterns(
        string
    )

    for match in region:
        info[match.span()] = {"region": match.captures()[0]}
    for match in county:
        info[match.span()] = {"county": match.captures()[0]}
    for match in area:
        info[match.span()] = {"area": match.captures()[0]}
    for match in place:
        info[match.span()] = {"places": match.captures()[0]}
    for match in date:
        info[match.span()] = {"date": match.captures()[0]}
    for match in time:
        info[match.span()] = {"time": match.captures()[0]}

    ordered_info = OrderedDict(sorted(info.items()))

    frame = pd.DataFrame.from_dict(ordered_info.values())

    data = frame.apply(fill_dataframe, axis=0)

    if "date" in data.columns:
        data.date = pd.to_datetime(data.date, infer_datetime_format=True, dayfirst=True)

    if "time" in data.columns:
        data = data[data.time.notnull()].reset_index(drop=True)
        data.time = data.apply(time_cleaner, axis=1)
        data.time = data.time.str.lstrip()
        data.time = data.time.str.replace("—", "-")
        data.time = data.time.str.replace("--", "-")
        # data.time = data.time.str.replace("a.m", "a.m.", regex=False)

    if "county" in data.columns:
        data.county = data.county.str.lstrip()
        data.county = data.apply(county_cleaner, axis=1)

    if "region" in data.columns:
        data.region = data.apply(region_cleaner, axis=1)
        data.region = data.region.str.replace(
            pat=r"\d", repl="", regex=True
        )
        data.region = data.region.str.lstrip()

    if "area" in data.columns:
        data.area = data.area.str.lstrip()

    if "places" in data.columns:
        data.places = data.places.str.lstrip()

    return data


def match_patterns(string: str) -> tuple[Any, Any, Any, Any, Any, Any]:
    """
        Match the patterns on input string
    """
    region = Patterns.REGIONS.finditer(string)
    county = Patterns.COUNTY.finditer(string)
    place = Patterns.PLACES.finditer(string)
    date = Patterns.DATE.finditer(string)
    time = Patterns.TIME.finditer(string)
    area = Patterns.AREAS.finditer(string)

    return region, county, place, date, time, area


def preprocess_image(image_path: str, brightness: float = 1.5, sharpness: float = 2) -> Optional[Image.Image]:
    """
        Resize, and threshold image, brighten, and sharpen in order to increase OCR accuracy
    """
    img = Image.open(image_path).convert("L")
    img = img.resize([2 * _ for _ in img.size], Image.Resampling.BICUBIC).point(lambda p: p > 75 and p + 100)
    enhancer = ImageEnhance.Brightness(img)
    image = enhancer.enhance(brightness)
    sharper = ImageEnhance.Sharpness(image=image)
    sharped_image = sharper.enhance(sharpness)

    return sharped_image


def fill_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
        The trick method... Impute missing rows
    """

    if df.name == "area" or df.name == "county" or df.name == "region":
        df = df.ffill()  # .bfill()
    elif df.name == "places":
        df = df.bfill()
    elif df.name == "date":
        df = df.bfill().ffill()
    return df


def county_cleaner(df: pd.DataFrame) -> pd.Series:
    if pd.isnull(df.county):
        return df.county
    elif "of" in df.county:
        return df.county.replace("of", "Parts of")
    else:
        return df.county


def time_cleaner(df: pd.DataFrame) -> pd.Series:
    """Append pm to end time in time pandas column"""

    if pd.isnull(df.time) or "p.m." in df.time:
        return df.time
    elif "p.m." not in df.time:
        return df.time + " p.m."
    else:
        return df.time


def region_cleaner(df: pd.DataFrame) -> pd.Series:
    if pd.isnull(df.region):
        return df.region
    elif "of" in df.region:
        return df.region.replace("of", "Parts of")
    else:
        return df.region


def save(data: pd.DataFrame, connection_engine: Any, table_name: str = "maintenance_schedule") -> Optional[int]:
    """Write the dataframe to database appending at the end"""

    return data.to_sql(name=table_name, con=connection_engine, if_exists="append", index=False)
