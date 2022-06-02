from typing import Dict, List
import src.util as util
import src.wrangle_bbr as wrangle_bbr
import pandas as pd
from pathlib import Path
import logging

from src.wrangle_bbr import CLEAN_USEFUL

# Basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def clean_building(building: List[Dict]) -> dict:
    return {wrangle_bbr.strip_bbr_tag(k): v for d in building for k, v in d.items()}


def clean_buildings(buildings: List[List[Dict]]) -> pd.DataFrame:
    return pd.DataFrame([clean_building(building) for building in buildings])


def clean_from_file(path: Path) -> pd.DataFrame:
    return clean_buildings(util.read_pickle(path))


def get_all_buildings(all_paths: List[Path]) -> pd.DataFrame:
    return pd.concat([clean_from_file(path) for path in all_paths])


if __name__ == "__main__":
    data_files = list(Path("data").glob("*v4.pkl"))

    logging.info("Reading data from %s files", len(data_files))
    fulldf = pd.concat(pd.DataFrame(util.read_pickle(path)) for path in data_files)
    logging.info("done!")
    fulldf.columns = [wrangle_bbr.strip_bbr_tag(k) for k in fulldf.columns]

    logging.info("Selecting subset of data...")
    choose_cols = [col for col in fulldf.columns if col in CLEAN_USEFUL]
    small_df = fulldf[choose_cols].reset_index(drop=True)
    wrangle_bbr.clean_columns(small_df)

    logging.info("filtering to only have fjernvarme and gas")
    dtypes = {
        "varmeinstallation": "int8",
        "opvarmningsmiddel": "float",
    }
    small_df = small_df.astype(dtypes)
    uses_gas = small_df["opvarmningsmiddel"].isin([2, 7]) | small_df[
        "varmeinstallation"
    ].isin([8])
    uses_fjernvarme = small_df["varmeinstallation"] == 1
    small_df = small_df[uses_gas | uses_fjernvarme]
    small_df["is_gas"] = uses_gas
    small_df["is_fjernvarme"] = uses_fjernvarme
    # remove columns that are not needed
    small_df = small_df.drop(["varmeinstallation", "opvarmningsmiddel",], axis=1)

    logging.info("filtering to only have koordinatsystems")
    small_df.dropna(subset=["koordinat"], inplace=True)

    logging.info("Writing file...")
    small_df.to_csv("data/select_bbr2.csv", index=False)
    logging.info("All done!")

    # small_df.drop_duplicates(subset=["byg057Opvarmningsmiddel", 'byg404Koordinat', 'husnummer'], inplace=True)

