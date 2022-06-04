import zipfile
from pathlib import Path
from lxml import etree
from functools import partial
from typing import Callable, Iterator, List, Dict, Any
import logging
import src.wrangle_bbr as wrangle_bbr


def zipped_xml_iterator(
    zip_file: Path, xml_file: str, parse_func: Callable
) -> Iterator[Any]:
    with zipfile.ZipFile(zip_file, "r") as z:
        with z.open(xml_file) as f:
            for obj in parse_func(f):
                yield obj


def get_target_tags(
    xml, target_tags: List[str], target_obj: str, stop_tag: str
) -> Iterator[Dict]:
    all_tags = target_tags + [target_obj, stop_tag]
    target_dict = {}
    for _, elem in etree.iterparse(xml, tag=all_tags):
        if elem.tag == stop_tag:
            logging.info(f"Found stop tag {stop_tag}")
            break
        if elem.tag == target_obj:
            yield target_dict
            target_dict = {}
            elem.clear()
        if elem.text is not None:
            target_dict[elem.tag] = elem.text
        elem.clear()

