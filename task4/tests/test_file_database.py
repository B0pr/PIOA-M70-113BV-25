import unittest
import os
import json
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.file_database import FileDatabase

class TestFileDatabase(unittest.TestCase):
    
    def setUp(self):
        self.test_filename = "test_data.json"
        self.db = FileDatabase(self.test_filename)
        self.db.clear()
    
    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
    
    def test_add_student_saves_to_file(self):
        self.db.add_student("Иван", "PIOA-70", 4.5)
        self.assertTrue(os.path.exists(self.test_filename))
        with open(self.test_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data["students"]), 1)
        self.assertEqual(data["students"][0]["name"], "Иван")
    
    def test_load_from_file(self):
        self.db.add_student("Петр", "PIOA-71", 3.8)
        db2 = FileDatabase(self.test_filename)
        self.assertEqual(len(db2), 1)
        self.assertEqual(db2.get_all()[0].name, "Петр")
    
    def test_add_student_valid(self):
        student = self.db.add_student("Анна", "PIOA-70", 4.8)
        self.assertEqual(student.name, "Анна")
        self.assertEqual(len(self.db), 1)
    
    def test_add_student_invalid_grade(self):
        with self.assertRaises(ValueError):
            self.db.add_student("Анна", "PIOA-70", 6.0)
    
    def test_get_all_empty(self):
        self.assertEqual(self.db.get_all(), [])
    
    def test_find_by_name(self):
        self.db.add_student("Ольга", "PIOA-70", 4.5)
        results = self.db.find_by_filter("name", "Ольга")
        self.assertEqual(len(results), 1)
    
    def test_find_by_group(self):
        self.db.add_student("Иван", "PIOA-70", 4.5)
        self.db.add_student("Петр", "PIOA-71", 3.8)
        results = self.db.find_by_filter("group", "PIOA-70")
        self.assertEqual(len(results), 1)
    
    def test_clear(self):
        self.db.add_student("Иван", "PIOA-70", 4.5)
        self.db.clear()
        self.assertEqual(len(self.db), 0)
        with open(self.test_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data["students"]), 0)

if __name__ == "__main__":
    unittest.main()