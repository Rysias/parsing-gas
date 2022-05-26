"""
Finds the crs in the big XML
"""
import logging
import src.extract as extract
import src.util as util
from pathlib import Path

# basic config
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


def main():
    ZIP_FILE, XML_FILE = util.get_zip_and_xml(Path("data"))
    logging.info("Starting to parse")
    for _, elem in extract.find_first_tag(
        ZIP_FILE, XML_FILE, tag="byg406Koordinatsystem"
    ):
        logging.info(f"Found crs: {elem}")
        # write crs to txt file
        with open("crs.txt", "w") as f:
            f.write(elem)
        return

    pass


if __name__ == "__main__":
    main()
