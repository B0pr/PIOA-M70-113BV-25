from database.table import Table

class ConsoleUI:
    """Класс консольного интерфейса"""
    
    def __init__(self):
        self.db = Table()
    
    def _print_student(self, student):
        """Вывод одного студента"""
        print(f"  ID: {student.id} | Имя: {student.name} | Группа: {student.group} | Балл: {student.grade}")
    
    def _print_students(self, students):
        """Вывод списка студентов"""
        if not students:
            print("  Нет записей")
            return
        for s in students:
            self._print_student(s)
    
    def _add_student(self):
        """Добавление студента"""
        print("\n--- Добавление студента ---")
        try:
            name = input("Введите имя: ").strip()
            group = input("Введите группу: ").strip()
            grade_input = input("Введите средний балл (0-5): ").strip()
            grade = float(grade_input)
            
            student = self.db.add_student(name, group, grade)
            print(f"\n✅ Студент добавлен с ID: {student.id}")
            
        except ValueError as e:
            print(f"\n❌ Ошибка: {e}")
        except Exception as e:
            print(f"\n❌ Непредвиденная ошибка: {e}")
    
    def _show_all(self):
        """Показать всех студентов"""
        print("\n--- Список всех студентов ---")
        students = self.db.get_all()
        self._print_students(students)
    
    def _search(self):
        """Поиск студентов"""
        print("\n--- Поиск студентов ---")
        print("Искать по:")
        print("  1. ID")
        print("  2. Имени")
        print("  3. Группе")
        print("  4. Баллу")
        print("  5. По нескольким полям")
        
        search_choice = input("Выберите тип поиска (1-5): ").strip()
        
        try:
            if search_choice == "1":
                id_input = input("Введите ID: ").strip()
                student_id = int(id_input)
                results = self.db.find_by_filter("id", student_id)
                print(f"\n--- Результаты поиска (ID={student_id}) ---")
                self._print_students(results)
            
            elif search_choice == "2":
                name = input("Введите имя: ").strip()
                results = self.db.find_by_filter("name", name)
                print(f"\n--- Результаты поиска (Имя={name}) ---")
                self._print_students(results)
            
            elif search_choice == "3":
                group = input("Введите группу: ").strip()
                results = self.db.find_by_filter("group", group)
                print(f"\n--- Результаты поиска (Группа={group}) ---")
                self._print_students(results)
            
            elif search_choice == "4":
                grade_input = input("Введите балл: ").strip()
                grade = float(grade_input)
                results = self.db.find_by_filter("grade", grade)
                print(f"\n--- Результаты поиска (Балл={grade}) ---")
                self._print_students(results)
            
            elif search_choice == "5":
                filters = {}
                print("Оставьте поле пустым, чтобы пропустить")
                
                name = input("Имя (Enter - пропустить): ").strip()
                if name:
                    filters["name"] = name
                
                group = input("Группа (Enter - пропустить): ").strip()
                if group:
                    filters["group"] = group
                
                grade_input = input("Балл (Enter - пропустить): ").strip()
                if grade_input:
                    filters["grade"] = float(grade_input)
                
                if not filters:
                    print("\n❌ Не указано ни одного критерия поиска")
                else:
                    results = self.db.find_by_multiple_filters(filters)
                    print(f"\n--- РезульConsoleUIтаты поиска ---")
                    self._print_students(results)
            
            else:
                print("\n❌ Неверный выбор")
        
        except ValueError as e:
            print(f"\n❌ Ошибка ввода: {e}")
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
    def _sort_students(self):
        """Сортировка студентов"""
        print("\n--- Сортировка студентов ---")
        print("Сортировать по:")
        print("  1. ID")
        print("  2. Имени")
        print("  3. Группе")
        print("  4. Баллу")
        
        field_choice = input("Выберите поле (1-4): ").strip()
        
        field_map = {
            "1": "id",
            "2": "name", 
            "3": "group",
            "4": "grade"
        }
        
        if field_choice not in field_map:
            print("\n❌ Неверный выбор")
            return
        
        field = field_map[field_choice]
        
        print("\nНаправление сортировки:")
        print("  1. По возрастанию")
        print("  2. По убыванию")
        
        order_choice = input("Выберите направление (1-2): ").strip()
        reverse = (order_choice == "2")
        
        try:
            sorted_students = self.db.sort_by(field, reverse)
            print(f"\n--- Сортировка по полю '{field}' ({'убывание' if reverse else 'возрастание'}) ---")
            self._print_students(sorted_students)
        except ValueError as e:
            print(f"\n❌ Ошибка: {e}")

    def run(self):
        """Запуск интерфейса"""
        while True:
            print("\n" + "="*40)
            print("        БАЗА ДАННЫХ СТУДЕНТОВ")
            print("="*40)
            print("1. Добавить студента")
            print("2. Показать всех студентов")
            print("3. Поиск по фильтру")
            print("4. Сортировка")
            print("5. Выйти")
            print("-"*40)
            
            choice = input("Выберите действие (1-5): ").strip()
            
            if choice == "1":
                self._add_student()
            elif choice == "2":
                self._show_all()
            elif choice == "3":
                self._search()
            elif choice == "4":
                self._sort_students()
            elif choice == "5":
                print("\nДо свидания!")
                break
            else:
                print("\n❌ Неверный выбор, попробуйте снова")