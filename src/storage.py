# src/storage.py

import json
import csv

def save_to_json(data, filename: str) -> None:
    """Save the crawled data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f)

def save_to_csv(data, filename: str) -> None:
    """Save the crawled data to a CSV file."""
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)
