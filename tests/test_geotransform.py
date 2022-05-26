import numpy as np
import pandas as pd
import src.geo_transform as gt


def test_transform_to_wgs84():
    point = "POINT(516612.96 6142758.59)"
    lat, long = gt.transform_to_wgs84(point)
    assert 40.0 < lat < 70
    assert 5 < long < 15


def test_transform_all_wgs84():
    points = pd.Series(["POINT(516612.96 6142758.59)", "POINT(721498.37 6192612.49)"])
    lats, longs = gt.points_to_wgs84(points)
    assert 40.0 < lats[0] < 70
    assert 5 < longs[0] < 15


def test_transform_ints_wgs84():
    points = pd.Series(["POINT(516612 6142758)", "POINT(721498 6192612)"])
    lats, longs = gt.points_to_wgs84(points)
    assert 40.0 < lats[0] < 70
    assert 5 < longs[0] < 15


# TODO Fix OUT OF RANGE ERROR

