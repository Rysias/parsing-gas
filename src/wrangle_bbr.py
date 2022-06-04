import pandas as pd
from typing import Union


def strip_bbr_tag(tag: str) -> str:
    return tag.replace("{http://data.gov.dk/schemas/bbr}", "")


def format_bbr_tag(tag: str) -> str:
    """
    """
    return "{http://data.gov.dk/schemas/bbr}" + tag


def camel_to_snake(col: Union[pd.Series, pd.Index]) -> pd.Series:
    return col.str.replace("([a-z])([A-Z])", r"\1_\2", regex=True).str.lower()


def remove_bygning(cols: pd.Index) -> pd.Index:
    return cols.str.replace(r"byg\d+", "", regex=True)


def clean_columns(df: pd.DataFrame) -> None:
    df.columns = camel_to_snake(remove_bygning(df.columns))


USEFUL_COLS = [
    "{http://data.gov.dk/schemas/bbr}husnummer",
    "{http://data.gov.dk/schemas/bbr}id_lokalId",
    "{http://data.gov.dk/schemas/bbr}byg021BygningensAnvendelse",
    "{http://data.gov.dk/schemas/bbr}byg056Varmeinstallation",
    "{http://data.gov.dk/schemas/bbr}byg057Opvarmningsmiddel",
    "{http://data.gov.dk/schemas/bbr}byg404Koordinat",
    "{http://data.gov.dk/schemas/bbr}byg406Koordinatsystem",
    "{http://data.gov.dk/schemas/bbr}byg134KvalitetAfKoordinatsæt",
    "{http://data.gov.dk/schemas/bbr}kommunekode",
]

CLEAN_USEFUL = [strip_bbr_tag(col) for col in USEFUL_COLS]
