from pois.file_parsers import BasePoIFileParser
from pois.models import POI
from pois.parser_factories import CSVPoIParserFactory, JSONPoIParserFactory, XMLPoIParserFactory
from typing import Iterator, List
from pois.row_parsers import PoIData


class PoIObjectCreationHandler:

    def create_poi_objects(self, items: list[PoIData]) -> list[POI]:
        objs = [self.get_poi_obj(item) for item in items]
        POI.objects.bulk_create(objs)
        return objs

    def get_poi_obj(self, item: PoIData) -> POI:
        poi = POI(
            name = item.name,
            external_id = item.external_id,
            category = item.category,
            poi_latitude = item.latitude,
            poi_longitude = item.longitude,
            ratings = item.ratings,
        )
        poi.set_avg_rating()
        return poi


class PoIFileUploader:
    DB_UPLOAD_BATCH_SIZE = 10000

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_parser: BasePoIFileParser = self.get_file_parser()

    def get_file_parser(self) -> BasePoIFileParser:
        if self.file_path.endswith('.csv'):
            return CSVPoIParserFactory().create_file_parser()
        elif self.file_path.endswith('.json'):
            return JSONPoIParserFactory().create_file_parser()
        elif self.file_path.endswith('.xml'):
            return XMLPoIParserFactory().create_file_parser()
        
    def upload_to_db(self):
        for row_batch in self.get_bacthed_rows():
            PoIObjectCreationHandler().create_poi_objects(row_batch)

    def get_bacthed_rows(self) -> Iterator[List[PoIData]]:
        batch = []
        for parsed_row in self.file_parser.parsed_row_generator(self.file_path):
            batch.append(parsed_row)
            if len(batch) >= self.DB_UPLOAD_BATCH_SIZE:
                yield batch
                batch = []
        if batch:
            yield batch