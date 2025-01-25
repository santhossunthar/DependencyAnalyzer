from typing import Dict, List
import csv

class CSVWriter:
    def __init__(self, file_name: str, headers: List[str]):
        self.file_name = file_name
        self.headers = headers

        # Create the CSV file with headers if it doesn't exist
        with open(self.file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()

    def append_row(self, row: Dict):
        """Appends a single row to the CSV file."""
        with open(self.file_name, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writerow(row)
