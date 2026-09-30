class Table:
    def __init__(self):
        self.data = []
        self.next_id = 1
    
    def add_student(self, name: str, group: str, grade: float) -> dict:
        student = {
            "id": self.next_id,
            "name": name,
            "group": group,
            "grade": grade
        }
        self.data.append(student)
        self.next_id += 1
        return student
    
    def get_all(self) -> list:
        return self.data
    
    def find_by_filter(self, field: str, value) -> list:
        if field not in ["id", "name", "group", "grade"]:
            raise ValueError(f"Неизвестное поле: {field}")
        
        results = []
        for student in self.data:
            if student[field] == value:
                results.append(student)
        return results
    
    def find_by_multiple_filters(self, filters: dict) -> list:
        results = self.data
        for field, value in filters.items():
            if field not in ["id", "name", "group", "grade"]:
                raise ValueError(f"Неизвестное поле: {field}")
            results = [s for s in results if s[field] == value]
        return results

    def update(self, student_id: int, name: str = None, group: str = None, grade: float = None) -> bool:
        """Обновление данных студента по ID"""
        for student in self.data:
            if student["id"] == student_id:
                if name is not None:
                    if not name or not name.strip():
                        raise ValueError("Имя не может быть пустым")
                    student["name"] = name.strip()
                if group is not None:
                    if not group or not group.strip():
                        raise ValueError("Группа не может быть пустой")
                    student["group"] = group.strip()
                if grade is not None:
                    if not isinstance(grade, (int, float)):
                        raise ValueError("Балл должен быть числом")
                    if grade < 0 or grade > 5:
                        raise ValueError("Балл должен быть от 0 до 5")
                    student["grade"] = float(grade)
                return True
        raise ValueError(f"Студент с ID {student_id} не найден")

    def delete(self, student_id: int) -> bool:
        """Удаление студента по ID"""
        for i, student in enumerate(self.data):
            if student["id"] == student_id:
                del self.data[i]
                return True
        raise ValueError(f"Студент с ID {student_id} не найден")