import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.console import ConsoleUI
from database import FileDatabase, CSVFileDatabase

def main():
    print("=" * 40)
    print("   ВЫБОР ТИПА БАЗЫ ДАННЫХ")
    print("=" * 40)
    print("1. In-memory (данные не сохраняются)")
    print("2. File-based JSON (сохранение в JSON)")
    print("3. File-based CSV (сохранение в CSV)")
    print("-" * 40)
    
    choice = input("Выберите тип (1-3): ").strip()
    
    if choice == "2":
        db = FileDatabase("students_data.json")
        print("\n✅ Используется JSON БД (students_data.json)")
    elif choice == "3":
        db = CSVFileDatabase("students_data.csv")
        print("\n✅ Используется CSV БД (students_data.csv)")
    else:
        from database.table import Table
        db = Table()
        print("\n⚠️  Используется in-memory БД (данные НЕ сохранятся)")
    
    ui = ConsoleUI(db)
    ui.run()

if __name__ == "__main__":
    main()