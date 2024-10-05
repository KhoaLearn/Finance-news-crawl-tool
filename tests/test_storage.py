# tests/test_storage.py

import unittest
import os
from src.storage import save_to_json, save_to_csv

class TestStorage(unittest.TestCase):
    
    def test_save_to_json(self):
        """Test saving data to a JSON file."""
        data = {"key": "value"}
        filename = 'test.json'
        save_to_json(data, filename)
        
        self.assertTrue(os.path.exists(filename))  # Ensure the file is created
        
        # Clean up after test
        os.remove(filename)
    
    def test_save_to_csv(self):
        """Test saving data to a CSV file."""
        data = [["column1", "column2"], ["data1", "data2"]]
        filename = 'test.csv'
        save_to_csv(data, filename)
        
        self.assertTrue(os.path.exists(filename))  # Ensure the file is created
        
        # Clean up after test
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
