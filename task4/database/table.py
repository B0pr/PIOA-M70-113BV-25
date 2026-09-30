"""Общий класс Table — базовая логика для всех хранилищ студентов."""

import math

class Table:
    """Базовая таблица студентов. Хранит данные в памяти и реализует
    общую логику: валидацию, добавление, поиск, удаление.

    Наследники (FileDatabase, CSVFileDatabase) отвечают только
    за загрузку/сохранение данных в конкретный формат файла.
    """

    VALID_FIELDS = ["id", "name", "group", "grade"]

    def __init__(self):
        self._data = []
        self._next_id = 1

    # ---------- Валидация ----------

    @staticmethod
    def _validate(name: str, group: str, grade) -> None:
        """Проверяет корректность данных студента.

        Бросает ValueError, если что-то не так.
        """
        if not name or not name.strip():
            raise ValueError("Имя не может быть пустым")
        if not group or not group.strip():
            raise ValueError("Группа не может быть пустой")
        if isinstance(grade, bool) or not isinstance(grade, (int, float)):
            raise ValueError("Балл должен быть числом")
        if not math.isfinite(grade):
            raise ValueError("Балл должен быть конечным числом (не NaN, не inf)")
        if grade < 0 or grade > 5:
            raise ValueError("Балл должен быть от 0 до 5")

    @classmethod
    def _check_field(cls, field: str) -> None:
        if field not in cls.VALID_FIELDS:
            raise ValueError(f"Неизвестное поле: {field}")

    # ---------- Основные операции ----------

    def add_student(self, name: str, group: str, grade) -> "Student":
        """Добавляет студента, сохраняет состояние, возвращает его."""
        self._validate(name, group, grade)
        student = self._make_student(self._next_id, name.strip(), group.strip(), float(grade))
        self._data.append(student)
        self._next_id += 1
        self._save()
        return student

    def get_all(self) -> list:
        """Возвращает независимую копию списка студентов."""
        return list(self._data)

    def get_by_id(self, student_id: int) -> "Student":
        for student in self._data:
            if student.id == student_id:
                return student
        raise ValueError(f"Студент с ID {student_id} не найден")

    def find_by_filter(self, field: str, value) -> list:
        """Поиск по одному полю. Возвращает независимый список."""
        self._check_field(field)

        if field == "id":
            # Единое правило: ID — целое число, дробное не совпадает.
            if isinstance(value, bool) or not isinstance(value, int):
                if isinstance(value, float) and not value.is_integer():
                    return []
            try:
                return [self.get_by_id(int(value))]
            except (ValueError, TypeError):
                return []

        results = []
        for student in self._data:
            if field == "name" and isinstance(value, str) and student.name.lower() == value.lower():
                results.append(student)
            elif field == "group" and isinstance(value, str) and student.group.lower() == value.lower():
                results.append(student)
            elif field == "grade" and student.grade == value:
                results.append(student)
        return results

    def find_by_multiple_filters(self, filters: dict) -> list:
        """Поиск по нескольким полям. Возвращает независимый список."""
        results = list(self._data)  # копия, а не ссылка на внутренний список
        for field, value in filters.items():
            self._check_field(field)
            if field == "name":
                results = [s for s in results if isinstance(value, str) and s.name.lower() == value.lower()]
            elif field == "group":
                results = [s for s in results if isinstance(value, str) and s.group.lower() == value.lower()]
            elif field == "grade":
                results = [s for s in results if s.grade == value]
            elif field == "id":
                if isinstance(value, float) and not value.is_integer():
                    results = []
                else:
                    results = [s for s in results if s.id == value]
        return results

    def clear(self) -> None:
        """Очищает таблицу и сохраняет пустое состояние."""
        self._data = []
        self._next_id = 1
        self._save()

    def __len__(self) -> int:
        return len(self._data)

    # ---------- Точки расширения для наследников ----------

    def _make_student(self, student_id: int, name: str, group: str, grade: float) -> "Student":
        """Создаёт объект Student. Наследники могут переопределить."""
        from models.student import Student
        return Student(student_id, name, group, grade)

    def _save(self) -> None:
        """Сохранение. В базовом классе — ничего. Наследники переопределяют."""
        pass