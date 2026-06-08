from models.student import Student

class Table:
    """Класс таблицы БД, работающий со студентами"""
    
    def __init__(self):
        self._data = []
        self._next_id = 1
    
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
            raise ValueError(f"Неизвестное поле: {field}. Доступные поля: {valid_fields}")
        
        results = []
        for student in self._data:
            if field == "id":
                if student.id == value:
                    results.append(student)
            elif field == "name":
                if student.name.lower() == value.lower():
                    results.append(student)
            elif field == "group":
                if student.group.lower() == value.lower():
                    results.append(student)
            elif field == "grade":
                if student.grade == value:
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
    
    def __len__(self):
        return len(self._data)
    
    def sort_by(self, field: str, reverse: bool = False) -> list:
        """
        Сортировка студентов по указанному полю
        field: 'id', 'name', 'group', 'grade'
        reverse: False - по возрастанию, True - по убыванию
        """
        valid_fields = ["id", "name", "group", "grade"]
        if field not in valid_fields:
            raise ValueError(f"Неизвестное поле: {field}. Доступные: {valid_fields}")
        
        sorted_data = sorted(self._data, key=lambda s: getattr(s, field), reverse=reverse)
        return sorted_data