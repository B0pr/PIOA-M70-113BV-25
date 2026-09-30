import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.student import Student

class FileDatabase:
    """Файловая БД студентов с сохранением в JSON"""
    
    def __init__(self, filename="data.json"):
        self.filename = filename
        self._data = []
        self._next_id = 1
        self._load()
    
    def _load(self):
        """Загрузка данных из JSON-файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._data = [Student.from_dict(item) for item in data.get("students", [])]
                    self._next_id = data.get("next_id", 1)
            except (json.JSONDecodeError, IOError, UnicodeDecodeError) as e:
                print(f"Ошибка загрузки: {e}")
                self._data = []
                self._next_id = 1
        else:
            self._data = []
            self._next_id = 1
    
    def _save(self):
        """Сохранение данных в JSON-файл"""
        try:
            data = {
                "students": [s.to_dict() for s in self._data],
                "next_id": self._next_id
            }
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка сохранения: {e}")
    
    def add_student(self, name: str, group: str, grade: float) -> Student:
        """Добавление студента"""
        if not name or not name.strip():
            raise ValueError("Имя не может быть пустым")
        if not group or not group.strip():
            raise ValueError("Группа не может быть пустой")
        if not isinstance(grade, (int, float)):
            raise ValueError("Балл должен быть числом")
        if grade < 0 or grade > 5:
            raise ValueError("Балл должен быть от 0 до 5")
        
        student = Student(self._next_id, name.strip(), group.strip(), float(grade))
        self._data.append(student)
        self._next_id += 1
        self._save()
        return student
    
    def get_all(self) -> list:
        """Получить всех студентов"""
        return self._data.copy()
    
    def get_by_id(self, student_id: int) -> Student:
        """Поиск студента по ID"""
        for student in self._data:
            if student.id == student_id:
                return student
        raise ValueError(f"Студент с ID {student_id} не найден")
    
    def find_by_filter(self, field: str, value) -> list:
        """Поиск по одному полю"""
        valid_fields = ["id", "name", "group", "grade"]
        if field not in valid_fields:
            raise ValueError(f"Неизвестное поле: {field}")
        
        results = []
        for student in self._data:
            if field == "id" and student.id == value:
                results.append(student)
            elif field == "name" and student.name.lower() == value.lower():
                results.append(student)
            elif field == "group" and student.group.lower() == value.lower():
                results.append(student)
            elif field == "grade" and student.grade == value:
                results.append(student)
        return results
    
    def find_by_multiple_filters(self, filters: dict) -> list:
        """Поиск по нескольким полям"""
        results = self._data
        for field, value in filters.items():
            if field == "name":
                results = [s for s in results if s.name.lower() == value.lower()]
            elif field == "group":
                results = [s for s in results if s.group.lower() == value.lower()]
            elif field == "grade":
                results = [s for s in results if s.grade == value]
            elif field == "id":
                results = [s for s in results if s.id == value]
            else:
                raise ValueError(f"Неизвестное поле: {field}")
        return results
    
    def clear(self):
        """Очистка таблицы (для тестов)"""
        self._data = []
        self._next_id = 1
        self._save()
    
    def __len__(self):
        return len(self._data)