import src.wrangle_bbr as wrangle
import pandas as pd


def test_strip_bbr_tag():
    assert (
        wrangle.strip_bbr_tag("{http://data.gov.dk/schemas/bbr}husnummer")
        == "husnummer"
    )


def test_clean_columns():
    df = pd.DataFrame({"byg021BygningensAnvendelse": [1, 2, 3]})
    wrangle.clean_columns(df)
    assert df.columns[0] == "bygningens_anvendelse"
