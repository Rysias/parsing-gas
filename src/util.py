import pickle
from pathlib import Path
from typing import Optional, Tuple


def create_dir(path: str) -> Path:
    new_dir = Path(path)
    if not new_dir.exists():
        new_dir.mkdir()
    return new_dir


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
    if not path.parent.exists():
        path.parent.mkdir()
    with open(path, "wb") as f:
        pickle.dump(data, f)


def read_pickle(path: Path) -> object:
    with open(path, "rb") as f:
        return pickle.load(f)
