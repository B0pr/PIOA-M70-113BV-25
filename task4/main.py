import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.console import ConsoleUI
from database import FileDatabase

def main():
    print("=" * 40)
    print("   ВЫБОР ТИПА БАЗЫ ДАННЫХ")
    print("=" * 40)
    print("1. In-memory (данные не сохраняются)")
    print("2. File-based (сохранение в JSON)")
    print("-" * 40)
    
    choice = input("Выберите тип (1-2): ").strip()
    
    if choice == "2":
        db = FileDatabase("students_data.json")
        print("\n✅ Используется файловая БД (данные сохраняются в students_data.json)")
    else:
        from database.table import Table
        db = Table()
        print("\n⚠️  Используется in-memory БД (данные НЕ сохранятся после выхода)")
    
    ui = ConsoleUI(db)
    ui.run()

if __name__ == "__main__":
    main()