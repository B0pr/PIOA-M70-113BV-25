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