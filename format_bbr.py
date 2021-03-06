"""
Script for formatting the extracted pickled BBR data into a single csv file to be used for the analysis. 
"""

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


def df_to_zip(df: pd.DataFrame, filepath: Path) -> None:
    compression_opts = dict(method="zip", archive_name=f"{filepath.stem}.csv")
    df.to_csv(filepath, compression=compression_opts)


def select_subset(fulldf: pd.DataFrame) -> pd.DataFrame:
    fulldf.columns = [wrangle_bbr.strip_bbr_tag(k) for k in fulldf.columns]
    choose_cols = [col for col in fulldf.columns if col in CLEAN_USEFUL]
    small_df = fulldf[choose_cols].reset_index(drop=True)
    wrangle_bbr.clean_columns(small_df)
    return small_df


def main() -> None:
    data_files = list(Path("data").glob("*v4.pkl"))

    logging.info("Reading data from %s files", len(data_files))
    fulldf = pd.concat(pd.DataFrame(util.read_pickle(path)) for path in data_files)
    logging.info("done!")

    logging.info("Selecting subset of data...")
    small_df = select_subset(fulldf)

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
    outpath = Path("data/bbr_clean.zip")
    df_to_zip(small_df, outpath)
    logging.info("All done!")


if __name__ == "__main__":
    main()
