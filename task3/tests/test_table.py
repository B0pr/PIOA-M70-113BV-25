import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.table import Table

class TestTable(unittest.TestCase):
    
    def setUp(self):
        self.table = Table()
    
    def test_add_student_success(self):
        student = self.table.add_student("Иван Петров", "PIOA-70", 4.5)
        self.assertEqual(student.id, 1)
        self.assertEqual(student.name, "Иван Петров")
        self.assertEqual(student.group, "PIOA-70")
        self.assertEqual(student.grade, 4.5)
        self.assertEqual(len(self.table), 1)
    
    def test_add_student_empty_name(self):
        with self.assertRaises(ValueError):
            self.table.add_student("", "PIOA-70", 4.5)
    
    def test_add_student_empty_group(self):
        with self.assertRaises(ValueError):
            self.table.add_student("Иван", "", 4.5)
    
    def test_add_student_invalid_grade(self):
        with self.assertRaises(ValueError):
            self.table.add_student("Иван", "PIOA-70", 6.0)
    
    def test_get_all_empty(self):
        self.assertEqual(self.table.get_all(), [])
    
    def test_get_all_after_add(self):
        self.table.add_student("Иван", "PIOA-70", 4.5)
        self.table.add_student("Петр", "PIOA-71", 3.8)
        self.assertEqual(len(self.table.get_all()), 2)
    
    def test_get_by_id_success(self):
        student = self.table.add_student("Иван", "PIOA-70", 4.5)
        found = self.table.get_by_id(student.id)
        self.assertEqual(found.id, student.id)
    
    def test_get_by_id_not_found(self):
        with self.assertRaises(ValueError):
            self.table.get_by_id(999)
    
    def test_find_by_filter_name(self):
        self.table.add_student("Иван Петров", "PIOA-70", 4.5)
        self.table.add_student("Петр Иванов", "PIOA-70", 3.8)
        results = self.table.find_by_filter("name", "Иван Петров")
        self.assertEqual(len(results), 1)
    
    def test_find_by_filter_group(self):
        self.table.add_student("Иван", "PIOA-70", 4.5)
        self.table.add_student("Петр", "PIOA-71", 3.8)
        results = self.table.find_by_filter("group", "PIOA-70")
        self.assertEqual(len(results), 1)
    
    def test_find_by_filter_invalid_field(self):
        with self.assertRaises(ValueError):
            self.table.find_by_filter("invalid_field", "value")
    
    def test_find_by_multiple_filters(self):
        self.table.add_student("Иван", "PIOA-70", 4.5)
        self.table.add_student("Иван", "PIOA-71", 3.8)
        filters = {"name": "Иван", "grade": 4.5}
        results = self.table.find_by_multiple_filters(filters)
        self.assertEqual(len(results), 1)
    
    def test_clear_table(self):
        self.table.add_student("Иван", "PIOA-70", 4.5)
        self.table.add_student("Петр", "PIOA-70", 3.8)
        self.table.clear()
        self.assertEqual(len(self.table), 0)

if __name__ == "__main__":
    unittest.main()