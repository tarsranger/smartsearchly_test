import csv
import json
from .row_parsers import BasePoIFileRowParser, PoIData
from typing import Iterator
from lxml import etree


class BasePoIFileParser:

    def __init__(self, row_parser: BasePoIFileRowParser):
        self.row_parser = row_parser

    def parsed_row_generator(self, file_path: str) -> Iterator[PoIData]:
        """Parse the file and yield parsed rows."""
        raise NotImplementedError("Subclasses should implement this method")


class CSVPoIFileParser(BasePoIFileParser):

    def parsed_row_generator(self, file_path: str) -> Iterator[PoIData]:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                parsed_row = self.row_parser.parse_row(row)
                yield parsed_row


class JSONPoIFileParser(BasePoIFileParser):

    def parsed_row_generator(self, file_path: str) -> Iterator[PoIData]:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                parsed_row = self.row_parser.parse_row(item)
                yield parsed_row


class XMLPoIFileParser(BasePoIFileParser):

    def parsed_row_generator(self, file_path: str) -> Iterator[PoIData]:
        with open(file_path, "rb") as f:
            parser = etree.XMLParser(recover=True)
            tree = etree.parse(f, parser)
            root = tree.getroot()
            for record in root.iterfind("DATA_RECORD"):
                row = {child.tag: child.text for child in record}
                parsed_row = self.row_parser.parse_row(row)
                yield parsed_row