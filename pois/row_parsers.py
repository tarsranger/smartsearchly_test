from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class PoIData():
    external_id: str
    name: str
    latitude: float
    longitude: float
    category: str
    ratings: List[float]


class BasePoIFileRowParser:

    def parse_row(self, row: Dict[str, Any]) -> PoIData:
        self.row = row
        poi_data = PoIData(
            external_id = self.parse_poi_external_id(),
            name = self.parse_poi_name(),
            latitude = self.parse_poi_latitude(),
            longitude = self.parse_poi_longitude(),
            category = self.parse_poi_category(),
            ratings = self.parse_poi_ratings()
        )
        return poi_data
    
    def parse_poi_external_id(self):
        return NotImplementedError("Subclasses should implement this method")
    
    def parse_poi_name(self):   
        return NotImplementedError("Subclasses should implement this method")
    
    def parse_poi_latitude(self):
        return NotImplementedError("Subclasses should implement this method")  
    
    def parse_poi_longitude(self):      
        return NotImplementedError("Subclasses should implement this method")  
    
    def parse_poi_category(self):      
        return NotImplementedError("Subclasses should implement this method")
    
    def parse_poi_ratings(self):      
        return NotImplementedError("Subclasses should implement this method")


class CSVPoIFileRowParser(BasePoIFileRowParser):
    
    def parse_poi_external_id(self) -> str:
        return str(self.row.get("poi_id", "")).strip()
    
    def parse_poi_name(self) -> str:
        return str(self.row.get("poi_name", "")).strip()
    
    def parse_poi_latitude(self) -> float:
        try:
            return float(self.row.get("poi_latitude", ""))
        except ValueError:
            return float("nan")
    
    def parse_poi_longitude(self) -> float:
        try:
            return float(self.row.get("poi_longitude", ""))
        except ValueError:
            return float("nan")
    
    def parse_poi_category(self) -> str:
        return str(self.row.get("poi_category", "")).strip()

    def parse_poi_ratings(self) -> List[float]:
        ratings_str = str(self.row.get("poi_ratings", ""))
        ratings_str = ratings_str.replace(" ", "").replace("{", "").replace("}", "")
        if not ratings_str:
            return []
        try:
            return [float(r) for r in ratings_str.split(",") if r]
        except ValueError:
            return []
        

class JSONPoIFileRowParser(BasePoIFileRowParser):

    def parse_poi_external_id(self) -> str:
        return str(self.row.get("id", "")).strip()

    def parse_poi_name(self) -> str:
        return str(self.row.get("name", "")).strip()

    def parse_poi_latitude(self) -> float:
        coordinates = self.row.get("coordinates", {})
        latitude = coordinates.get("latitude", "")
        try:
            return float(latitude)
        except (ValueError, TypeError):
            return float("nan")

    def parse_poi_longitude(self) -> float:
        coordinates = self.row.get("coordinates", {})
        longitude = coordinates.get("longitude", "")
        try:
            return float(longitude)
        except (ValueError, TypeError):
            return float("nan")

    def parse_poi_category(self) -> str:
        return str(self.row.get("category", "")).strip()
    
    def parse_poi_ratings(self) -> List[float]:
        ratings = self.row.get("ratings", [])
        if not isinstance(ratings, list):
            return []
        try:
            return [float(r) for r in ratings if isinstance(r, (int, float, str)) and str(r).strip() != ""]
        except ValueError:
            return []
        

class XMLPoIFileRowParser(BasePoIFileRowParser):

    def parse_poi_external_id(self) -> str:
        return str(self.row.get("pid", "")).strip()

    def parse_poi_name(self) -> str:
        return str(self.row.get("pname", "")).strip()

    def parse_poi_latitude(self) -> float:
        try:
            return float(self.row.get("platitude", ""))
        except (ValueError, TypeError):
            return float("nan")

    def parse_poi_longitude(self) -> float:
        try:
            return float(self.row.get("plongitude", ""))
        except (ValueError, TypeError):
            return float("nan")

    def parse_poi_category(self) -> str:
        return str(self.row.get("pcategory", "")).strip()

    def parse_poi_ratings(self) -> List[float]:
        ratings_str = str(self.row.get("pratings", "")).replace(" ", "")
        if not ratings_str:
            return []
        try:
            return [float(r) for r in ratings_str.split(",") if r]
        except ValueError:
            return []