import os
import json
import csv
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from pois.models import POI
from pois.file_uploader import PoIFileUploader


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_paths', nargs='+', type=str)

    def handle(self, *args, **options):
        for file_path in options['file_paths']:
            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
                continue
            
            if not file_path.endswith(('.csv', '.json', '.xml')):
                self.stdout.write(self.style.ERROR(f'Unsupported file type: {file_path}'))

            PoIFileUploader(file_path).upload_to_db()
            self.stdout.write(self.style.SUCCESS(f'Successfully processed file: {file_path}'))


    def import_csv(self, file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                poi = POI(
                    internal_id=row['poi_id'],
                    name=row['poi_name'],
                    external_id=row['poi_id'],  # Assuming external ID is the same as internal ID
                    category=row['poi_category'],
                    avg_rating=row['poi_ratings']
                )
                poi.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully imported CSV: {file_path}'))

    def import_json(self, file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                poi = POI(
                    internal_id=item['id'],
                    name=item['name'],
                    external_id=item['id'],  # Assuming external ID is the same as internal ID
                    category=item['category'],
                    avg_rating=item['ratings']
                )
                poi.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully imported JSON: {file_path}'))

    def import_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        for poi in root.findall('poi'):
            poi_data = {
                'internal_id': poi.find('pid').text,
                'name': poi.find('pname').text,
                'external_id': poi.find('pid').text,  # Assuming external ID is the same as internal ID
                'category': poi.find('pcategory').text,
                'avg_rating': poi.find('pratings').text
            }
            poi_instance = POI(
                internal_id=poi_data['internal_id'],
                name=poi_data['name'],
                external_id=poi_data['external_id'],
                category=poi_data['category'],
                avg_rating=poi_data['avg_rating']
            )
            poi_instance.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully imported XML: {file_path}'))