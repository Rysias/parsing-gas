"""
Script for processing the huge BBR xml file. Concretely, we want to extract: 
- the location of each building
- the heating type
- the building id
"""
from pathlib import Path
import logging
import argparse
import src.wrangle_bbr as wrangle_bbr
import src.extract as extract
import src.util as util
from src.wrangle_bbr import USEFUL_COLS
from functools import partial

# basic logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

# TODO
# - add bolig fields

SAVE_EVERY = 100_000


def extract_bygning_clean(
    zip_file: Path, xml_file: str,
):
    TARGET_OBJ = wrangle_bbr.format_bbr_tag("Bygning")
    STOP_TAG = wrangle_bbr.format_bbr_tag("BygningList")
    TARGET_TAGS = USEFUL_COLS
    extract_func = partial(
        extract.get_target_tags,
        target_tags=TARGET_TAGS,
        target_obj=TARGET_OBJ,
        stop_tag=STOP_TAG,
    )
    building_list = []
    i = 1
    logging.info("Starting to parse")

    for build_dict in extract.zipped_xml_iterator(zip_file, xml_file, extract_func):
        if "{http://data.gov.dk/schemas/bbr}byg056Varmeinstallation" in build_dict:
            building_list.append(build_dict)
        if i == 1:
            logging.info("Found first building!")
        elif i % SAVE_EVERY == 0:
            logging.info(f"{i} buildings extracted")
            util.write_pickle(
                building_list, Path(f"data/bygningslist{i // SAVE_EVERY}v4.pkl")
            )
            building_list.clear()
        i += 1
    util.write_pickle(building_list, Path(f"data/bygningslist_finalv4.pkl"))


def main(args):
    INPUT_DIR = Path(args.data_dir)
    try:
        ZIP_PATH, XML_NAME = util.get_zip_and_xml(INPUT_DIR)
    except ValueError:
        logging.error("Could not find zip file")
        return

    extract_bygning_clean(ZIP_PATH, XML_NAME)


if __name__ == "__main__":
    # add a description
    parser = argparse.ArgumentParser(description="what the program does")

    # add the arguments
    parser.add_argument(
        "--data-dir", help="path to were to find the input file", default="input"
    )
    args = parser.parse_args()
    main(args)
