from pois.file_parsers import BasePoIFileParser, CSVPoIFileParser, JSONPoIFileParser, XMLPoIFileParser
from pois.row_parsers import BasePoIFileRowParser, CSVPoIFileRowParser, JSONPoIFileRowParser, XMLPoIFileRowParser


class PoIParserFactory:

    def create_file_parser(self) -> BasePoIFileParser:
        raise NotImplementedError

    def create_row_parser(self) -> BasePoIFileRowParser:
        raise NotImplementedError


class CSVPoIParserFactory(PoIParserFactory):

    def create_file_parser(self):
        return CSVPoIFileParser(self.create_row_parser())

    def create_row_parser(self):
        return CSVPoIFileRowParser()
    

class JSONPoIParserFactory(PoIParserFactory):

    def create_file_parser(self):
        return JSONPoIFileParser(self.create_row_parser())

    def create_row_parser(self):
        return JSONPoIFileRowParser()
    

class XMLPoIParserFactory(PoIParserFactory):

    def create_file_parser(self):
        return XMLPoIFileParser(self.create_row_parser())

    def create_row_parser(self):
        return XMLPoIFileRowParser()