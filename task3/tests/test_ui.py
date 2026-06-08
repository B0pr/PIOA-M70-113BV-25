import unittest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.console import ConsoleUI

class TestConsoleUI(unittest.TestCase):
    
    def setUp(self):
        self.ui = ConsoleUI()
    
    def test_add_student_direct(self):
        """Тест добавления студента напрямую (без моков)"""
        student = self.ui.db.add_student("Тест", "PIOA-70", 4.5)
        self.assertEqual(len(self.ui.db), 1)
        self.assertEqual(student.name, "Тест")
    
    def test_ui_initialization(self):
        self.assertIsNotNone(self.ui.db)
        self.assertEqual(len(self.ui.db), 0)
    
    @patch('builtins.input', side_effect=["2", "4"])
    @patch('builtins.print')
    def test_show_all_empty(self, mock_print, mock_input):
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

if __name__ == "__main__":
    unittest.main()