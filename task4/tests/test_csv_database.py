import unittest
import os
import csv
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.csv_database import CSVFileDatabase

class TestCSVFileDatabase(unittest.TestCase):
    
    def setUp(self):
        self.test_filename = "test_csv_data.csv"
        self.db = CSVFileDatabase(self.test_filename)
        self.db.clear()
    
    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
    
    def test_add_student_saves_to_csv(self):
        self.db.add_student("Иван", "PIOA-70", 4.5)
        self.assertTrue(os.path.exists(self.test_filename))
        with open(self.test_filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["name"], "Иван")
    
    def test_load_from_csv(self):
        self.db.add_student("Петр", "PIOA-71", 3.8)
        db2 = CSVFileDatabase(self.test_filename)
        self.assertEqual(len(db2), 1)
        self.assertEqual(db2.get_all()[0].name, "Петр")
    
    def test_get_by_id_with_index(self):
        student = self.db.add_student("Анна", "PIOA-70", 4.8)
        found = self.db.get_by_id(student.id)
        self.assertEqual(found.name, "Анна")
    
    def test_find_by_filter_uses_index_for_id(self):
        self.db.add_student("Ольга", "PIOA-70", 4.5)
        results = self.db.find_by_filter("id", 1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Ольга")
    
    def test_clear(self):
        self.db.add_student("Иван", "PIOA-70", 4.5)
        self.db.clear()
        self.assertEqual(len(self.db), 0)

if __name__ == "__main__":
    unittest.main()