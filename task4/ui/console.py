class ConsoleUI:
    """Класс консольного интерфейса"""
    
    def __init__(self, database):
        self.db = database
    
    def _print_student(self, student):
        print(f"  ID: {student.id} | Имя: {student.name} | Группа: {student.group} | Балл: {student.grade}")
    
    def _print_students(self, students):
        if not students:
            print("  Нет записей")
            return
        for s in students:
            self._print_student(s)
    
    def _add_student(self):
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
        print("\n--- Список всех студентов ---")
        students = self.db.get_all()
        self._print_students(students)
    
    def _search(self):
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
                    print(f"\n--- Результаты поиска ---")
                    self._print_students(results)
            
            else:
                print("\n❌ Неверный выбор")
        
        except ValueError as e:
            print(f"\n❌ Ошибка ввода: {e}")
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
    
    def run(self):
        while True:
            print("\n" + "="*40)
            print("        БАЗА ДАННЫХ СТУДЕНТОВ")
            print("="*40)
            print("1. Добавить студента")
            print("2. Показать всех студентов")
            print("3. Поиск по фильтру")
            print("4. Выйти")
            print("-"*40)
            
            choice = input("Выберите действие (1-4): ").strip()
            
            if choice == "1":
                self._add_student()
            elif choice == "2":
                self._show_all()
            elif choice == "3":
                self._search()
            elif choice == "4":
                print("\nДо свидания!")
                break
            else:
                print("\n❌ Неверный выбор, попробуйте снова")