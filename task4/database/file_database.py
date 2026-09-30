"""Файловая БД студентов с сохранением в JSON.

Наследуется от Table — вся общая логика (валидация, поиск, добавление)
берётся из родителя. Здесь реализованы только загрузка и сохранение
в JSON, включая сохранение схемы таблицы.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.table import Table
from models.student import Student

class FileDatabase(Table):
    """Файловая БД студентов с сохранением в JSON."""

    def __init__(self, filename: str = "data.json"):
        super().__init__()
        self.filename = filename
        self._load()

    # ---------- Загрузка / сохранение ----------

    def _load(self) -> None:
        """Загрузка данных из JSON-файла.

        При ошибке чтения состояние НЕ сбрасывается в пустое —
        бросается исключение, чтобы нельзя было случайно уничтожить данные.
        """
        if not os.path.exists(self.filename):
            self._data = []
            self._next_id = 1
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError, UnicodeDecodeError) as e:
            raise IOError(f"Не удалось загрузить БД '{self.filename}': {e}")

        self._data = [Student.from_dict(item) for item in data.get("students", [])]
        self._next_id = data.get("next_id", 1)

    def _save(self) -> None:
        """Сохранение данных в JSON-файл вместе со схемой таблицы.

        При ошибке — бросает IOError, чтобы вызывающий код знал о проблеме
        и не считал операцию успешной.
        """
        data = {
            "schema": {
                "columns": ["id", "name", "group", "grade"],
                "next_id": self._next_id,
            },
            "students": [s.to_dict() for s in self._data],
            "next_id": self._next_id,
        }
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise IOError(f"Не удалось сохранить БД '{self.filename}': {e}")