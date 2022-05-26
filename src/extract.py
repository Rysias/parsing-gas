import zipfile
from pathlib import Path
from lxml import etree
from functools import partial
from typing import Callable, Iterator, List, Dict, Any
import logging
import src.wrangle_bbr as wrangle_bbr


def iterparse_zip(
    zip_file: Path, xml_file: str, parse_func: Callable = etree.iterparse
):
    with zipfile.ZipFile(zip_file, "r") as z:
        with z.open(xml_file) as f:
            for event, elem in parse_func(f):
                yield event, elem


def zipped_xml_iterator(
    zip_file: Path, xml_file: str, parse_func: Callable
) -> Iterator[Any]:
    with zipfile.ZipFile(zip_file, "r") as z:
        with z.open(xml_file) as f:
            for obj in parse_func(f):
                yield obj


def find_first_tag(zip_file: Path, xml_file: str, tag: str) -> Iterator[str]:
    parse_func = partial(etree.iterparse, tag=wrangle_bbr.format_bbr_tag(tag))
    for _, elem in iterparse_zip(zip_file, xml_file, parse_func=parse_func):
        yield elem.text


def get_target_tags(
    xml, target_tags: List[str], target_obj: str, stop_tag: str
) -> Iterator[Dict]:
    all_tags = target_tags + [target_obj]
    target_dict = {}
    for _, elem in etree.iterparse(xml, tag=all_tags):
        if elem.tag == stop_tag:
            logging.info(f"Found stop tag {stop_tag}")
            return
        if elem.tag == target_obj:
            yield target_dict
            target_dict = {}
            elem.clear()
        if elem.text is not None:
            target_dict[elem.tag] = elem.text
        elem.clear()

