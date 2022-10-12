from collections import OrderedDict
from typing import Any, Optional

import pandas as pd

from .config import configs
from .database import engine
from .patterns import Patterns


class Functions:
    """
    Utility functions applied to the dataframe for various actions
    including cleaning, extracting text, imputing null rows, writing to database, 
    and more. This class is not meant to be subclassed
    """

    @staticmethod
    def extract_text(path: str) -> pd.DataFrame:
        """Actual workhorse method"""
        with open(path, "r", encoding=configs.ENCODING) as f:
            string = " ".join([line.rstrip() for line in f.readlines()])
            string = string.lower().replace(
                "mr.", "Mr").replace(
                "st.", "St").replace(
                "mt.", "Mt"
            )

        info = {}

        region, county, place, date, time, area = Functions.match_patterns(
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

        data = frame.apply(Functions.fill_dataframe, axis=0)

        if "date" in data.columns:
            data.date = pd.to_datetime(data.date, format="%d.%m.%Y")

        if "time" in data.columns:
            data = data[data.time.notnull()].reset_index(drop=True)
            data.time = data.apply(Functions.time_cleaner, axis=1)
            data.time = data.time.str.lstrip()
            data.time = data.time.str.replace("—", "-")
            data.time = data.time.str.replace("--", "-")
            # data.time = data.time.str.replace("a.m", "a.m.", regex=False)

        if "county" in data.columns:
            data.county = data.apply(Functions.county_cleaner, axis=1)

        if "region" in data.columns:
            data.region = data.apply(Functions.region_cleaner, axis=1)

        return data

    @staticmethod
    def match_patterns(string: str) -> tuple[Any, Any, Any, Any, Any, Any]:
        region = Patterns.REGIONS.finditer(string)
        county = Patterns.COUNTY.finditer(string)
        place = Patterns.PLACES.finditer(string)
        date = Patterns.DATE.finditer(string)
        time = Patterns.TIME.finditer(string)
        area = Patterns.AREAS.finditer(string)

        return region, county, place, date, time, area

    @staticmethod
    def fill_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """The trick method... Impute missing rows"""
        if df.name == "area" or df.name == "county" or df.name == "region":
            df = df.ffill()  # .bfill()
        elif df.name == "places":
            df = df.bfill()
        elif df.name == "date":
            df = df.bfill().ffill()
        return df

    @staticmethod
    def county_cleaner(df: pd.DataFrame) -> pd.Series:
        if pd.isnull(df.county):
            return df.county
        elif "of" in df.county:
            return df.county.replace("of", "Parts of")
        else:
            return df.county

    @staticmethod
    def time_cleaner(df: pd.DataFrame) -> pd.Series:
        """Append pm to end time in time pandas column"""
        if pd.isnull(df.time) or "p.m." in df.time:
            return df.time
        elif "p.m." not in df.time:
            return df.time + " p.m."
        else:
            return df.time

    @staticmethod
    def region_cleaner(df: pd.DataFrame) -> pd.Series:
        if pd.isnull(df.region):
            return df.region
        elif "of" in df.region:
            return df.region.replace("of", "Parts of")
        else:
            return df.region

    @staticmethod
    def save(df: pd.DataFrame) -> Optional[int]:
        """Write the dataframe to database appending at the end"""
        return df.to_sql(name="maintenance_schedule", con=engine, if_exists="append", index_label="id")
