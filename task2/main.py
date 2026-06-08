from database import Table

def print_student(student):
    print(f"  ID: {student['id']} | Имя: {student['name']} | Группа: {student['group']} | Балл: {student['grade']}")

def print_students(students):
    if not students:
        print("  Нет записей")
        return
    for s in students:
        print_student(s)

def main():
    db = Table()
    
    while True:
        print("\n" + "="*40)
        print("        БАЗА ДАННЫХ СТУДЕНТОВ")
        print("="*40)
        print("1. Добавить студента")
        print("2. Показать всех студентов")
        print("3. Поиск по фильтру")
        print("4. Обновить студента")
        print("5. Удалить студента")
        print("6. Выйти")
        print("-"*40)
        
        choice = input("Выберите действие (1-6): ").strip()
        
        if choice == "1":
            print("\n--- Добавление студента ---")
            try:
                name = input("Введите имя: ").strip()
                if not name:
                    raise ValueError("Имя не может быть пустым")
                
                group = input("Введите группу: ").strip()
                if not group:
                    raise ValueError("Группа не может быть пустой")
                
                grade_input = input("Введите средний балл (число): ").strip()
                grade = float(grade_input)
                
                student = db.add_student(name, group, grade)
                print(f"\n✅ Студент добавлен с ID: {student['id']}")
                
            except ValueError as e:
                print(f"\n❌ Ошибка: {e}")
            except Exception as e:
                print(f"\n❌ Непредвиденная ошибка: {e}")
        
        elif choice == "2":
            print("\n--- Список всех студентов ---")
            students = db.get_all()
            print_students(students)
        
        elif choice == "3":
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
                    results = db.find_by_filter("id", student_id)
                    print(f"\n--- Результаты поиска (ID={student_id}) ---")
                    print_students(results)
                
                elif search_choice == "2":
                    name = input("Введите имя: ").strip()
                    results = db.find_by_filter("name", name)
                    print(f"\n--- Результаты поиска (Имя={name}) ---")
                    print_students(results)
                
                elif search_choice == "3":
                    group = input("Введите группу: ").strip()
                    results = db.find_by_filter("group", group)
                    print(f"\n--- Результаты поиска (Группа={group}) ---")
                    print_students(results)
                
                elif search_choice == "4":
                    grade_input = input("Введите балл: ").strip()
                    grade = float(grade_input)
                    results = db.find_by_filter("grade", grade)
                    print(f"\n--- Результаты поиска (Балл={grade}) ---")
                    print_students(results)
                
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
                        results = db.find_by_multiple_filters(filters)
                        print(f"\n--- Результаты поиска ---")
                        print_students(results)
                
                else:
                    print("\n❌ Неверный выбор")
            
            except ValueError as e:
                print(f"\n❌ Ошибка ввода: {e}")
            except Exception as e:
                print(f"\n❌ Ошибка: {e}")
        
        elif choice == "4":
            print("\n--- Обновление студента ---")
            try:
                id_input = input("Введите ID студента: ").strip()
                student_id = int(id_input)
                
                print("Оставьте поле пустым, чтобы не менять")
                name = input("Новое имя (Enter - пропустить): ").strip()
                group = input("Новая группа (Enter - пропустить): ").strip()
                grade_input = input("Новый балл (Enter - пропустить): ").strip()
                
                grade = float(grade_input) if grade_input else None
                name = name if name else None
                group = group if group else None
                
                db.update(student_id, name, group, grade)
                print(f"\n✅ Студент с ID {student_id} обновлён")
                
            except ValueError as e:
                print(f"\n❌ Ошибка: {e}")
            except Exception as e:
                print(f"\n❌ Непредвиденная ошибка: {e}")
        
        elif choice == "5":
            print("\n--- Удаление студента ---")
            try:
                id_input = input("Введите ID студента для удаления: ").strip()
                student_id = int(id_input)
                
                students = db.find_by_filter("id", student_id)
                if students:
                    print(f"Будет удалён: ", end="")
                    print_student(students[0])
                    confirm = input("Подтвердите удаление (y/n): ").strip().lower()
                    if confirm == 'y':
                        db.delete(student_id)
                        print(f"\n✅ Студент с ID {student_id} удалён")
                    else:
                        print("\n❌ Удаление отменено")
                else:
                    print(f"\n❌ Студент с ID {student_id} не найден")
                
            except ValueError as e:
                print(f"\n❌ Ошибка: {e}")
            except Exception as e:
                print(f"\n❌ Непредвиденная ошибка: {e}")
        
        elif choice == "6":
            print("\nДо свидания!")
            break
        
        else:
            print("\n❌ Неверный выбор, попробуйте снова")

if __name__ == "__main__":
    main()