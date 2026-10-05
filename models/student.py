class Student:
    """Класс, представляющий студента"""
    
    def __init__(self, student_id: int, name: str, group: str, grade: float):
        self.id = student_id
        self.name = name
        self.group = group
        self.grade = grade
    
    def to_dict(self) -> dict:
        """Преобразование в словарь"""
        return {
            "id": self.id,
            "name": self.name,
            "group": self.group,
            "grade": self.grade
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Student':
        """Создание студента из словаря"""
        return Student(data["id"], data["name"], data["group"], data["grade"])
    
    def __repr__(self):
        return f"Student(id={self.id}, name={self.name}, group={self.group}, grade={self.grade})"