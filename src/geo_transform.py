from typing import List, Tuple
import re
import pandas as pd
import numpy as np
import utm  # type: ignore


def find_floats(string: str) -> Tuple[float, float]:
    pattern = re.compile(r"[-+]?\d*\.\d+|\d+")
    return tuple(float(match) for match in pattern.findall(string))


def transform_to_wgs84(point: str, zone_num=32, zone_letter="N") -> Tuple[float, float]:
    x, y = find_floats(point)
    lat, lon = utm.to_latlon(x, y, zone_num, zone_letter)
    return lat, lon


def points_to_coords(points: pd.Series) -> pd.DataFrame:
    return pd.DataFrame(
        points.str.lstrip("POINT(").str.rstrip(")").str.split().tolist(),
        columns=["x", "y"],
    ).astype(float)


def get_xy_from_points(points: pd.Series) -> Tuple[np.ndarray, np.ndarray]:
    temp_df = points_to_coords(points)
    x = temp_df["x"].values
    y = temp_df["y"].values
    return x, y  # type: ignore


def points_to_wgs84(
    points: pd.Series, zone_num=32, zone_letter="N"
) -> Tuple[np.ndarray, np.ndarray]:
    x, y = get_xy_from_points(points)
    lat, lon = utm.to_latlon(x, y, zone_num, zone_letter)
    return lat, lon
