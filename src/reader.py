import csv
import json
from typing import List, Dict


class DataReader:
    @staticmethod
    def read_csv(file_path: str) -> List[Dict]:
        """Reads a CSV file and returns a list of dictionaries."""
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    @staticmethod
    def read_json(file_path: str) -> List[Dict]:
        """Reads a JSON file and returns a list of dictionaries."""
        with open(file_path, mode="r", encoding="utf-8") as file:
            return json.load(file)
