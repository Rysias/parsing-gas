from typing import List
import pandas as pd
import numpy as np
import networkx as nx
import osmnx as ox  # type: ignore
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

KOMMUNEKODE = Path("data/meta/kommunekode.csv")


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


def nearest_nodes(G, df: pd.DataFrame, node_type: str) -> List[int]:
    nodes, dists = ox.distance.nearest_nodes(
        G,
        df[f"{node_type}_x"].tolist(),
        df[f"{node_type}_y"].tolist(),
        return_dist=True,
    )
    logging.info("average %s error: %s", node_type, np.mean(dists))
    return nodes


def calculate_road_dists(
    graph: nx.Graph, source_nodes: List[int], target_nodes: List[int]
) -> np.ndarray:
    lengths = np.zeros(len(source_nodes))
    assert lengths.shape == (len(source_nodes),)
    for i, (source, target) in tqdm(enumerate(zip(source_nodes, target_nodes))):
        length = nx.shortest_path_length(
            G=graph, source=source, target=target, weight="length"
        )
        lengths[i] += length
    return lengths


def main(args: argparse.Namespace):
    KOMMUNE_ID = args.kommune_id
    INPUT_PATH = Path(args.input_path)
    logging.info("loading data...")
    df = pd.read_csv(INPUT_PATH)
    kommune_df = df.loc[df["kommunekode"] == KOMMUNE_ID, :]
    Gp = projected_kommune_graph(KOMMUNE_ID)

    gas_nodes = nearest_nodes(Gp, kommune_df, "gas")
    fjern_nodes = nearest_nodes(Gp, kommune_df, "fjernvarme")
    lengths = calculate_road_dists(Gp, source_nodes=gas_nodes, target_nodes=fjern_nodes)

    logging.info("Writing results to file...")
    kommune_df = kommune_df.assign(road_dist=lengths)
    kommune_df.to_csv(f"out/{KOMMUNE_ID}_road_dist.csv", index=False)

    logging.info("Saving graph to plots/...")
    ox.plot.plot_graph(
        Gp, show=False, save=True, filename=f"plots/{KOMMUNE_ID}_graph.png"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyse road distances in a kommune.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--kommune-id", type=int, required=True, help="The kommune id to analyse."
    )
    parser.add_argument(
        "--input-path", type=str, default="output/gas_fjernvarme_xy.csv"
    )
    args = parser.parse_args()
    main(args)
