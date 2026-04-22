import sys
from scanner import Scanner, ScannerError
from parser import Parser, ParserError
from semantic import SemanticAnalyzer, SemanticError

TESTS = {
   
    
    "Пример 1 (Простая инициализация)": """
        int x = 10;
        int y = 20;
        int z;
        z = x + y;
    """,
    
    "Пример 2 (Приоритет операций)": """
        int a = 5;
        int b = 3;
        int result;
        result = a * b + 2;
        int value;
        value = a * (b + 2);
    """,
    
    "Пример 3 (Множественные операции)": """
        int one = 100;
        int two = 25;
        int three = 10;
        int sum;
        sum = one + two - three;
        int res;
        res = sum / 5 * 2;
    """,
    
    "Пример 4 (Последовательность вычислений)": """
        int i = 0;
        i = i + 1;
        i = i * 10;
        i = i - 5;
        int res;
        res = i / 2;
    """,

    "Объявление без инициализации": """
        int x;
    """,

    "Объявление с инициализацией": """
        int x = 42;
    """,

    "Присваивание существующей переменной": """
        int x = 10;
        x = 25;
    """,

   
    
    "Сложение": """
        int a = 5;
        int b = 3;
        int c;
        c = a + b;
    """,
    
    "Вычитание": """
        int x = 20;
        int y = 8;
        int z;
        z = x - y;
    """,
    
    "Умножение": """
        int a = 6;
        int b = 7;
        int result;
        result = a * b;
    """,
    
    "Деление (целочисленное)": """
        int x = 10;
        int y = 3;
        int z;
        z = x / y;
    """,
    
    "Приоритет * над +": """
        int a = 2;
        int b = 3;
        int c = 4;
        int result;
        result = a + b * c;
    """,
    
    "Приоритет / над -": """
        int x = 20;
        int y = 4;
        int z = 2;
        int res;
        res = x - y / z;
    """,
    
    "Скобки меняют приоритет": """
        int a = 2;
        int b = 3;
        int c = 4;
        int result;
        result = (a + b) * c;
    """,

    
    
    "Унарный минус (число)": """
        int x;
        x = -15;
    """,
    
    "Унарный минус (переменная)": """
        int a = 10;
        int b;
        b = -a;
    """,
    
    "Двойной унарный минус": """
        int x = 7;
        int y;
        y = --x;
    """,
    
    "Унарный минус в выражении": """
        int a = 5;
        int b = 3;
        int c;
        c = a + -b;
    """,
    
    "Унарный минус со скобками": """
        int x = 10;
        int y = 4;
        int z;
        z = -(x - y);
    """,

  
    
    "Цепочка сложений": """
        int a = 1;
        int b = 2;
        int c = 3;
        int d = 4;
        int sum;
        sum = a + b + c + d;
    """,
    
    "Смешанные операции": """
        int x = 10;
        int y = 3;
        int z = 2;
        int result;
        result = x * y + z / 2 - 5;
    """,
    
    "Вложенные скобки": """
        int a = 2;
        int b = 3;
        int c = 4;
        int d = 5;
        int res;
        res = ((a + b) * (c - d)) + 10;
    """,
    
    "Использование переменной в правой части": """
        int x = 5;
        x = x + 10;
    """,
    
    "Большое число": """
        int big = 999999;
        int small = 1000;
        int result;
        result = big / small;
    """,

   
    
    "ОШИБКА: необъявленная переменная": """
        int x = 10;
        y = x + 5;
    """,
    
    "ОШИБКА: повторное объявление": """
        int x = 5;
        int x = 10;
    """,
    
    "ОШИБКА: деление на ноль": """
        int x = 10;
        int y = 0;
        int z;
        z = x / y;
    """,
    
    "ОШИБКА: синтаксис (нет точки с запятой)": """
        int x = 10
        int y = 20;
    """,
    
    "ОШИБКА: неизвестный символ (@)": """
        int x = 10;
        x = x @ 5;
    """,
}

def run_test(name: str, code: str, should_fail: bool = False):
    """Функция запуска одного теста"""
    print(f"\n{'='*60}")

print(f"ТЕСТ: {name}")
    print(f"{'='*60}")
    print("Код:")
    for i, line in enumerate(code.strip().split('\n'), 1):
        print(f"  {i:2d} | {line}")
    print()
    
    try:
        # 1. Лексика
        scanner = Scanner(code)
        tokens = scanner.scan()
        
        # 2. Семантика
        analyzer = SemanticAnalyzer()
        
        # 3. Парсинг
        parser = Parser(tokens, analyzer)
        parser.parse()
        
        if should_fail:
            print("error ТЕСТ ПРОВАЛЕН: Ошибка ожидалась, но код выполнился успешно!")
        else:
            analyzer.print_results()
            print("complete ТЕСТ ПРОЙДЕН УСПЕШНО")
            
    except (ScannerError, ParserError, SemanticError) as e:
        if should_fail:
            print(f"complete ТЕСТ ПРОЙДЕН: Ошибка получена корректно -> {e}")
        else:
            print(f"error ТЕСТ ПРОВАЛЕН: {e}")
    except Exception as e:
        print(f"error НЕИЗВЕСТНАЯ ОШИБКА: {e}")

def run_all_tests():
    """Запуск всех тестов из словаря"""
    print("\nожидаем" * 30)
    print(" ЗАПУСК ВСЕХ ТЕСТОВ ")
    print("ожидаем" * 30)
    
    passed = 0
    failed = 0
    
    for name, code in TESTS.items():
        # Если имя начинается с "ОШИБКА", ожидаем падение (should_fail=True)
        is_error_test = name.startswith("ОШИБКА")
        
        try:
            run_test(name, code, should_fail=is_error_test)
            passed += 1
        except Exception:
            failed += 1
            
    print("\n успех" * 30)
    print(f" ИТОГО: Пройдено {passed}, Ошибок {failed} ")
    print(" успех" * 30 + "\n")

def main():
    print("\nпройдено" * 30)
    print(" ТРАНСЛЯТОР (Корчагин А., КМБО-05-23) ")
    print("пройдено" * 30)
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--all":
            run_all_tests()
        else:
            # Если передан просто аргумент, ищем тест по имени
            if arg in TESTS:
                run_test(arg, TESTS[arg])
            else:
                print(f"ошибка Тест '{arg}' не найден.")
    else:
        # Интерактивное меню
        print("\nВыберите режим:")
        print("  1 — Запустить ВСЕ тесты (--all)")
        print("  2 — Запустить конкретный тест")
        print("  3 — Выход")
        
        choice = input("\nВаш выбор (1-3): ").strip()
        
        if choice == '1':
            run_all_tests()
        elif choice == '2':
            print("\nСписок тестов:")
            for i, name in enumerate(TESTS.keys(), 1):
                print(f"  {i}. {name}")
            
            idx = input("\nВведите номер теста: ").strip()
            try:
                name = list(TESTS.keys())[int(idx) - 1]
                run_test(name, TESTS[name])
            except:
                print("ошибка Неверный номер.")
        elif choice == '3':
            print("Выход.")
        else:
            print("Неверный выбор.")

if name == "__main__":
    main() |