import unittest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.console import ConsoleUI
from database import FileDatabase

class TestConsoleUI(unittest.TestCase):
    
    def setUp(self):
        self.db = FileDatabase("test_ui_data.json")
        self.db.clear()
        self.ui = ConsoleUI(self.db)
    
    def tearDown(self):
        import os
        if os.path.exists("test_ui_data.json"):
            os.remove("test_ui_data.json")
    
    def test_ui_initialization(self):
        self.assertIsNotNone(self.ui.db)
        self.assertEqual(len(self.ui.db), 0)
    
    @patch('builtins.print')
    def test_show_all_empty(self, mock_print):
        self.ui._show_all()
        mock_print.assert_any_call("  Нет записей")
    
    def test_print_student(self):
        student = self.ui.db.add_student("Иван", "PIOA-70", 4.5)
        with patch('builtins.print') as mock_print:
            self.ui._print_student(student)
            mock_print.assert_called_once()
    
    def test_print_students_empty(self):
        with patch('builtins.print') as mock_print:
            self.ui._print_students([])
            mock_print.assert_called_with("  Нет записей")
    
    def test_add_student_through_ui(self):
        with patch('builtins.input', side_effect=["Иван", "PIOA-70", "4.5"]):
            with patch('builtins.print'):
                self.ui._add_student()
        self.assertEqual(len(self.ui.db), 1)
        student = self.ui.db.get_all()[0]
        self.assertEqual(student.name, "Иван")

if __name__ == "__main__":
    unittest.main()