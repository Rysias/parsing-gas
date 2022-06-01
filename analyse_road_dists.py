import pandas as pd
import numpy as np
import networkx as nx
import osmnx as ox
import csv
import argparse
from pathlib import Path
import logging
from tqdm import tqdm

ox.settings.log_console = True
ox.settings.use_cache = True

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

KOMMUNEKODE = Path("kommunekode.csv")


def csv_to_dict(csv_file: Path) -> dict:
    with open(csv_file, mode="r") as infile:
        reader = csv.reader(infile)
        return {rows[0]: rows[1] for rows in reader}


def get_kommunename(kommunekode: int) -> str:
    """
    Returns the name of the kommune with the given kommunekode.
    """
    return csv_to_dict(KOMMUNEKODE)[str(kommunekode)]


def projected_kommune_graph(kommune_id: int):
    """
    Returns a projected graph of the given kommune.
    """
    kommune_name = get_kommunename(kommune_id)
    logging.info("loading graph for %s", kommune_name)
    G = ox.graph_from_place(kommune_name, network_type="walk")
    logging.info("done! projecting graph..")
    projected_graph = ox.project_graph(G, to_crs="epsg:25832")
    logging.info("done!")
    return projected_graph


def main(args: argparse.Namespace):
    KOMMUNE_ID = args.kommune_id

    logging.info("loading data...")
    df = pd.read_csv("data/gas_fjernvarme_xy.csv")
    kommune_df = df[df["kommunekode"] == KOMMUNE_ID]
    Gp = projected_kommune_graph(KOMMUNE_ID)

    gas_nodes, gasdists = ox.distance.nearest_nodes(
        Gp,
        kommune_df["gas_x"].tolist(),
        kommune_df["gas_y"].tolist(),
        return_dist=True,
    )
    fjern_nodes, fjerndists = ox.distance.nearest_nodes(
        Gp,
        kommune_df["fjernvarme_x"].tolist(),
        kommune_df["fjernvarme_y"].tolist(),
        return_dist=True,
    )
    logging.info("average gas error: %s", np.mean(gasdists))
    logging.info("average fjern error: %s", np.mean(fjerndists))

    lengths = np.zeros(len(gas_nodes))
    assert lengths.shape == (len(gas_nodes),)
    for i, (gas, fjern) in tqdm(enumerate(zip(gas_nodes, fjern_nodes))):
        length = nx.shortest_path_length(
            G=Gp, source=gas, target=fjern, weight="length"
        )
        lengths[i] += length

    logging.info("All done! Writing results to file...")
    kommune_df = kommune_df.assign(road_dist=lengths)
    kommune_df.to_csv(f"out/{KOMMUNE_ID}_road_dist.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyse road distances in a kommune.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--kommune_id", type=int, default=306, help="The kommune id to analyse."
    )
    args = parser.parse_args()
    main(args)
