"""Файловая БД студентов с сохранением в CSV.

Наследуется от Table — общая логика в родителе.
Здесь реализованы загрузка, сохранение и индекс по ID.
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.table import Table
from models.student import Student

class CSVFileDatabase(Table):
    """Файловая БД студентов с сохранением в CSV."""

    SCHEMA = ["id", "name", "group", "grade"]

    def __init__(self, filename: str = "students_data.csv"):
        super().__init__()
        self.filename = filename
        self._index = {}
        self._load()

    # ---------- Загрузка / сохранение ----------

    def _load(self) -> None:
        """Загрузка данных из CSV-файла.

        При ошибке чтения состояние НЕ сбрасывается в пустое —
        бросается исключение, чтобы нельзя было потерять данные.
        """
        self._data = []
        self._index = {}
        self._next_id = 1

        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames != self.SCHEMA:
                    raise IOError(
                        f"Неверная схема CSV: ожидается {self.SCHEMA}, "
                        f"получено {reader.fieldnames}"
                    )
                for row in reader:
                    student = Student(
                        int(row["id"]),
                        row["name"],
                        row["group"],
                        float(row["grade"]),
                    )
                    self._data.append(student)
                    self._index[student.id] = student
                    if student.id >= self._next_id:
                        self._next_id = student.id + 1
        except (IOError, ValueError, KeyError, csv.Error) as e:
            raise IOError(f"Не удалось загрузить CSV '{self.filename}': {e}")

    def _save(self) -> None:
        """Сохранение данных в CSV вместе со схемой (заголовком).

        При ошибке — бросает IOError.
        """
        try:
            with open(self.filename, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.SCHEMA)
                writer.writeheader()
                for student in self._data:
                    writer.writerow(student.to_dict())
        except (IOError, csv.Error) as e:
            raise IOError(f"Не удалось сохранить CSV '{self.filename}': {e}")
        # Индекс поддерживаем в актуальном состоянии
        self._index = {s.id: s for s in self._data}

    # ---------- Переопределяем, чтобы поддерживать индекс ----------

    def add_student(self, name: str, group: str, grade):
        """Добавляет студента и обновляет индекс."""
        student = super().add_student(name, group, grade)
        self._index[student.id] = student
        return student

    def get_by_id(self, student_id: int):
        """Поиск по ID через индекс."""
        if student_id in self._index:
            return self._index[student_id]
        raise ValueError(f"Студент с ID {student_id} не найден")

    def clear(self) -> None:
        """Очищает таблицу, индекс и сохраняет пустое состояние."""
        self._data = []
        self._next_id = 1
        self._index = {}
        self._save()