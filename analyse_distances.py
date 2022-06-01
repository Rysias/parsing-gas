from typing import Tuple, Union
import pandas as pd
from sklearn.neighbors import KDTree
from pathlib import Path
import logging
import numpy as np
import src.geo_transform as gt

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
DATA_DIR = Path("data")


def find_distances(
    source_coords: pd.DataFrame, target_coords: pd.DataFrame
) -> Tuple[np.ndarray, np.ndarray]:
    """ Finds shortest distance from source to target """
    tree = KDTree(target_coords, leaf_size=30, metric="euclidean")

    # find the closest gas station to each fjernvarme
    distances, indices = tree.query(source_coords, k=1)
    return distances, indices


def main() -> None:
    logging.info("loading data..")
    df = pd.read_csv(DATA_DIR / "select_bbr2.csv")
    df = df[~df["koordinat"].isin(["POINT(0 0)", "POINT(0 0.5)"])]

    logging.info("deduplicating..")
    cols_to_use = ["husnummer", "koordinat", "kommunekode"]
    fjernvarme_koords = (
        df.loc[df["is_fjernvarme"], cols_to_use].drop_duplicates().dropna()
    )
    gas_koords = df.loc[df["is_gas"], cols_to_use].drop_duplicates().dropna()

    logging.info("Convertting to UTM 32N coordinates")
    gas_coords = gt.points_to_coords(gas_koords["koordinat"]).astype(float)
    fjernvarme_coords = gt.points_to_coords(fjernvarme_koords["koordinat"]).astype(
        float
    )

    logging.info("Finding distances...")
    gas_distances, gas_indices = find_distances(fjernvarme_coords, gas_coords)

    # Finding fjernvarme coordinates
    close_fjern = fjernvarme_coords.loc[gas_indices.reshape(-1), :].reset_index()

    logging.info("save data...")
    # Saving as dataframe
    output_df = pd.DataFrame(
        {
            "ID": gas_koords["husnummer"].reset_index(drop=True),
            "kommunekode": gas_koords["kommunekode"].reset_index(drop=True),
            "gas_x": gas_coords["x"],
            "gas_y": gas_coords["y"],
            "distance": gas_distances[:, 0],
            "fjernvarme_x": close_fjern["x"],
            "fjernvarme_y": close_fjern["y"],
        }
    )

    output_df.to_csv(DATA_DIR / "gas_fjernvarme_xy.csv", index=False)


if __name__ == "__main__":
    main()
