from ctypes import Union
import pickle
from pathlib import Path
from typing import Optional, Tuple


def find_zip_file(path: Path) -> Optional[Path]:
    return next(path.glob("*.zip"), None)


def get_zip_and_xml(dir: Path) -> Tuple[Path, str]:
    zip_path = find_zip_file(dir)
    if zip_path is None:
        print("Could not find zip file")
        return Path(""), ""
    xml_str = f"{zip_path.stem}.xml"
    return zip_path, xml_str


def write_pickle(data, path: Path):
    with open(path, "wb") as f:
        pickle.dump(data, f)


def read_pickle(path: Path) -> object:
    with open(path, "rb") as f:
        return pickle.load(f)