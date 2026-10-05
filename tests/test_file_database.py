import unittest
import os
import json
import math
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

    # ---------- Базовое ----------

    def test_add_student_saves_to_file(self):
        self.db.add_student("Иван", "PIOA-70", 4.5)
        self.assertTrue(os.path.exists(self.test_filename))
        with open(self.test_filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data["students"]), 1)
        self.assertEqual(data["students"][0]["name"], "Иван")

    def test_json_contains_schema(self):
        """Схема таблицы должна сохраняться в файл (замечание 3)."""
        self.db.add_student("Иван", "PIOA-70", 4.5)
        with open(self.test_filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("schema", data)
        self.assertEqual(data["schema"]["columns"], ["id", "name", "group", "grade"])

    def test_load_from_file(self):
        self.db.add_student("Петр", "PIOA-71", 3.8)
        db2 = FileDatabase(self.test_filename)
        self.assertEqual(len(db2), 1)
        self.assertEqual(db2.get_all()[0].name, "Петр")

    def test_add_student_valid(self):
        student = self.db.add_student("Анна", "PIOA-70", 4.8)
        self.assertEqual(student.name, "Анна")
        self.assertEqual(len(self.db), 1)

    def test_get_all_empty(self):
        self.assertEqual(self.db.get_all(), [])

    def test_get_all_returns_copy(self):
        """get_all не должен возвращать ссылку на внутренний список."""
        self.db.add_student("Иван", "PIOA-70", 4.5)
        copy = self.db.get_all()
        copy.clear()
        self.assertEqual(len(self.db), 1)

    def test_get_by_id(self):
        s = self.db.add_student("Иван", "PIOA-70", 4.5)
        found = self.db.get_by_id(s.id)
        self.assertEqual(found.name, "Иван")

    def test_get_by_id_missing(self):
        with self.assertRaises(ValueError):
            self.db.get_by_id(999)

    def test_clear(self):
        self.db.add_student("Иван", "PIOA-70", 4.5)
        self.db.clear()
        self.assertEqual(len(self.db), 0)
        with open(self.test_filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data["students"]), 0)

    # ---------- Валидация ----------

    def test_add_empty_name(self):
        with self.assertRaises(ValueError):
            self.db.add_student("", "PIOA-70", 4.5)

    def test_add_whitespace_name(self):
        with self.assertRaises(ValueError):
            self.db.add_student("   ", "PIOA-70", 4.5)

    def test_add_empty_group(self):
        with self.assertRaises(ValueError):
            self.db.add_student("Иван", "", 4.5)

    def test_add_non_numeric_grade(self):
        with self.assertRaises(ValueError):
            self.db.add_student("Иван", "PIOA-70", "abc")

    def test_add_bool_grade(self):
        with self.assertRaises(ValueError):
            self.db.add_student("Иван", "PIOA-70", True)

    def test_add_negative_grade(self):
        with self.assertRaises(ValueError):
            self.db.add_student("Иван", "PIOA-70", -1.0)

    def test_add_too_high_grade(self):
        with self.assertRaises(ValueError):
            self.db.add_student("Иван", "PIOA-70", 6.0)

    def test_add_nan_grade(self):
        """NaN не должен приниматься (замечание 8)."""
        with self.assertRaises(ValueError):
            self.db.add_student("Иван", "PIOA-70", math.nan)

    def test_add_inf_grade(self):
        with self.assertRaises(ValueError):
            self.db.add_student("Иван", "PIOA-70", math.inf)

    # ---------- Поиск поодному полю ----------

    def test_find_by_name(self):
        self.db.add_student("Ольга", "PIOA-70", 4.5)
        results = self.db.find_by_filter("name", "Ольга")
        self.assertEqual(len(results), 1)

    def test_find_by_name_case_insensitive(self):
        self.db.add_student("Ольга", "PIOA-70", 4.5)
        results = self.db.find_by_filter("name", "ольга")
        self.assertEqual(len(results), 1)

    def test_find_by_group(self):
        self.db.add_student("Иван", "PIOA-70", 4.5)
        self.db.add_student("Петр", "PIOA-71", 3.8)
        results = self.db.find_by_filter("group", "PIOA-70")
        self.assertEqual(len(results), 1)

    def test_find_by_grade(self):
        self.db.add_student("Иван", "PIOA-70", 4.5)
        results = self.db.find_by_filter("grade", 4.5)
        self.assertEqual(len(results), 1)

    def test_find_by_id_integer(self):
        s = self.db.add_student("Иван", "PIOA-70", 4.5)
        results = self.db.find_by_filter("id", s.id)
        self.assertEqual(len(results), 1)

    def test_find_by_id_float_fractional_not_found(self):
        """ID=1.9 не должен находить ID=1 (замечание 7)."""
        self.db.add_student("Иван", "PIOA-70", 4.5)
        results = self.db.find_by_filter("id", 1.9)
        self.assertEqual(results, [])

    def test_find_by_unknown_field(self):
        with self.assertRaises(ValueError):
            self.db.find_by_filter("unknown", "x")

    # ---------- Поиск по нескольким полям (замечание 2) ----------

    def test_find_by_multiple_filters_empty_dict(self):
        """Пустой фильтр возвращает независимую копию (замечание 9)."""
        self.db.add_student("Иван", "PIOA-70", 4.5)
        results = self.db.find_by_multiple_filters({})
        self.assertEqual(len(results), 1)
        results.clear()
        self.assertEqual(len(self.db), 1)  # не должно влиять на внутренний список

    def test_find_by_multiple_filters_name_and_group(self):
        self.db.add_student("Иван", "PIOA-70", 4.5)
        self.db.add_student("Иван", "PIOA-71", 4.5)
        self.db.add_student("Петр", "PIOA-70", 4.5)
        results = self.db.find_by_multiple_filters({"name": "Иван", "group": "PIOA-70"})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].group, "PIOA-70")

    def test_find_by_multiple_filters_grade(self):
        self.db.add_student("Иван", "PIOA-70", 4.5)
        self.db.add_student("Петр", "PIOA-70", 3.0)
        results = self.db.find_by_multiple_filters({"grade": 4.5})
        self.assertEqual(len(results), 1)

    def test_find_by_multiple_filters_id(self):
        s = self.db.add_student("Иван", "PIOA-70", 4.5)
        results = self.db.find_by_multiple_filters({"id": s.id})
        self.assertEqual(len(results), 1)

    def test_find_by_multiple_filters_id_fractional(self):
        self.db.add_student("Иван", "PIOA-70", 4.5)
        results = self.db.find_by_multiple_filters({"id": 1.9})
        self.assertEqual(results, [])

    def test_find_by_multiple_filters_unknown_field(self):
        with self.assertRaises(ValueError):
            self.db.find_by_multiple_filters({"unknown": "x"})

    # ---------- Файловые ошибки (замечание 2) ----------

    def test_load_corrupted_json(self):
        """Битый JSON при загрузке -> IOError (замечание 5)."""
        with open(self.test_filename, "w", encoding="utf-8") as f:
            f.write("{ not valid json ")
        with self.assertRaises(IOError):
            FileDatabase(self.test_filename)

    def test_save_error_raises(self):
        """Ошибка записи -> IOError (замечание 4)."""
        self.db.filename = os.path.join("nonexistent_dir_xyz", "data.json")
        with self.assertRaises(IOError):
            self.db.add_student("Иван", "PIOA-70", 4.5)

if __name__ == "__main__":
    unittest.main()