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
