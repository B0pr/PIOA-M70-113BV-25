import csv
import os
from models.student import Student

class CSVFileDatabase:
    """Файловая БД студентов с сохранением в CSV"""
    
    def __init__(self, filename="students_data.csv"):
        self.filename = filename
        self._data = []
        self._next_id = 1
        self._index = {}  # индекс для быстрого поиска по ID
        self._load()
    
    def _load(self):
        """Загрузка данных из CSV-файла"""
        self._data = []
        self._index = {}
        
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        student = Student(
                            int(row['id']),
                            row['name'],
                            row['group'],
                            float(row['grade'])
                        )
                        self._data.append(student)
                        self._index[student.id] = student
                        if student.id >= self._next_id:
                            self._next_id = student.id + 1
            except Exception as e:
                print(f"Ошибка загрузки CSV: {e}")
                self._data = []
                self._next_id = 1
                self._index = {}
    
    def _save(self):
        """Сохранение данных в CSV-файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'name', 'group', 'grade'])
                writer.writeheader()
                for student in self._data:
                    writer.writerow(student.to_dict())
        except Exception as e:
            print(f"Ошибка сохранения CSV: {e}")
    
    def _rebuild_index(self):
        """Перестроить индекс (после изменений)"""
        self._index = {student.id: student for student in self._data}
    
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
        self._index[student.id] = student
        self._next_id += 1
        self._save()
        return student
    
    def get_all(self) -> list:
        """Получить всех студентов"""
        return self._data.copy()
    
    def get_by_id(self, student_id: int) -> Student:
        """Поиск студента по ID (с использованием индекса)"""
        if student_id in self._index:
            return self._index[student_id]
        raise ValueError(f"Студент с ID {student_id} не найден")
    
    def find_by_filter(self, field: str, value) -> list:
        """Поиск по одному полю"""
        valid_fields = ["id", "name", "group", "grade"]
        if field not in valid_fields:
            raise ValueError(f"Неизвестное поле: {field}")
        
        # Для ID используем индекс
        if field == "id":
            try:
                return [self.get_by_id(int(value))]
            except ValueError:
                return []
        
        results = []
        for student in self._data:
            if field == "name" and student.name.lower() == value.lower():
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
        """Очистка таблицы"""
        self._data = []
        self._next_id = 1
        self._index = {}
        self._save()
    
    def __len__(self):
        return len(self._data)