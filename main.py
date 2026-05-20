import sys
from scanner import Scanner, ScannerError
from parser import Parser, ParserError
from semantic import SemanticAnalyzer, SemanticError

TESTS = {
    # ==================== БАЗОВЫЕ КОНСТРУКЦИИ ====================
    "1. Простое объявление с инициализацией": """
        int x = 10;
    """,
    
    "2. Объявление без инициализации": """
        int x;
    """,
    
    "3. Присваивание переменной": """
        int x = 10;
        x = 20;
    """,
    
    "4. Объявление и использование": """
        int x = 10;
        int y = x;
    """,
    
    # ==================== АРИФМЕТИЧЕСКИЕ ОПЕРАЦИИ ====================
    "5. Сложение": """
        int a = 5;
        int b = 3;
        int c;
        c = a + b;
    """,
    
    "6. Вычитание": """
        int x = 20;
        int y = 8;
        int z;
        z = x - y;
    """,
    
    "7. Умножение": """
        int a = 6;
        int b = 7;
        int result;
        result = a * b;
    """,
    
    "8. Деление": """
        int x = 10;
        int y = 3;
        int z;
        z = x / y;
    """,
    
    # ==================== ПРИОРИТЕТ ОПЕРАЦИЙ ====================
    "9. Приоритет умножения над сложением": """
        int a = 2;
        int b = 3;
        int c = 4;
        int result;
        result = a + b * c;
    """,
    
    "10. Приоритет деления над вычитанием": """
        int x = 20;
        int y = 4;
        int z = 2;
        int res;
        res = x - y / z;
    """,
    
    "11. Скобки меняют приоритет": """
        int a = 2;
        int b = 3;
        int c = 4;
        int result;
        result = (a + b) * c;
    """,
    
    # ==================== СЛОЖНЫЕ ВЫРАЖЕНИЯ ====================
    "12. Цепочка сложений": """
        int a = 1;
        int b = 2;
        int c = 3;
        int d = 4;
        int sum;
        sum = a + b + c + d;
    """,
    
    "13. Смешанные операции": """
        int x = 10;
        int y = 3;
        int z = 2;
        int result;
        result = x * y + z / 2 - 5;
    """,
    
    "14. Вложенные скобки": """
        int a = 2;
        int b = 3;
        int c = 4;
        int d = 5;
        int res;
        res = ((a + b) * (c - d)) + 10;
    """,
    
    "15. Глубокая вложенность скобок": """
        int a = 1;
        int b = 2;
        int c = 3;
        int d = 4;
        int e = 5;
        int result;
        result = (((a + b) * c) - (d / e));
    """,
    
    # ==================== УНАРНЫЙ МИНУС ====================
    "16. Унарный минус (число)": """
        int x;
        x = -15;
    """,
    
    "17. Унарный минус (переменная)": """
        int a = 10;
        int b;
        b = -a;
    """,
    
    "18. Двойной унарный минус": """
        int x = 7;
        int y;
        y = --x;
    """,
    
    "19. Унарный минус в выражении": """
        int a = 5;
        int b = 3;
        int c;
        c = a + -b;
    """,
    
    "20. Унарный минус со скобками": """
        int x = 10;
        int y = 4;
        int z;
        z = -(x - y);
    """,
    
    "21. Унарный минус и умножение": """
        int a = 5;
        int b = 3;
        int c;
        c = -a * b;
    """,
    
    "22. Унарный минус и деление": """
        int x = 10;
        int y = 2;
        int z;
        z = -x / y;
    """,
    
    # ==================== ПОСЛЕДОВАТЕЛЬНЫЕ ОПЕРАЦИИ ====================
    "23. Последовательность вычислений": """
        int i = 0;
        i = i + 1;
        i = i * 10;
        i = i - 5;
        int res;
        res = i / 2;
    """,
    
    "24. Множественные присваивания": """
        int x = 0;
        x = 1;
        x = 2;
        x = 3;
        int y = x;
    """,
    
    # ==================== СЛОЖНЫЕ СЦЕНАРИИ ====================
    "25. Использование переменной в правой части": """
        int x = 5;
        x = x + 10;
    """,
    
    "26. Вычисление с большими числами": """
        int big = 999999;
        int small = 1000;
        int result;
        result = big / small;
    """,
    
    "27. Отрицательное число в выражении": """
        int a = 10;
        int b;
        b = a + -5;
    """,
    
    "28. Несколько унарных минусов": """
        int x = 5;
        int y;
        y = ---x;
    """,
    
    "29. Унарный минус и скобки": """
        int a = 10;
        int b = 3;
        int c;
        c = -(a - b) * 2;
    """,
    
    "30. Деление с остатком (целочисленное)": """
        int x = 17;
        int y = 5;
        int z;
        z = x / y;
    """,
    
    "31. Приоритет унарного минуса": """
        int a = 5;
        int b = 3;
        int c;
        c = -a + b;
    """,
    
    "32. Смешанные операции со скобками": """
        int x = 10;
        int y = 2;
        int z = 3;
        int res;
        res = (x + y) * (z - 1) / 2;
    """,
    
    "33. Сложные вложенные скобки": """
        int a = 1;
        int b = 2;
        int c = 3;
        int d = 4;
        int res;
        res = (((a + b) * (c - d)) + ((a * b) - (c + d)));
    """,
    
    "34. Цепочка с унарным минусом": """
        int a = 10;
        int b = 3;
        int c = 2;
        int result;
        result = -a + b * -c;
    """,
    
    # ==================== СЕМАНТИЧЕСКИЕ ОШИБКИ ====================
    "35. ОШИБКА: необъявленная переменная": """
        int x = 10;
        y = x + 5;
    """,
    
    "36. ОШИБКА: повторное объявление": """
        int x = 5;
        int x = 10;
    """,
    
    "37. ОШИБКА: деление на ноль (литерал)": """
        int x = 10;
        int y;
        y = x / 0;
    """,
    
    "38. ОШИБКА: деление на ноль (переменная)": """
        int x = 10;
        int y = 0;
        int z;
        z = x / y;
    """,
    
    "39. ОШИБКА: использование необъявленной в выражении": """
        int x;
        int y = x + 5;
    """,
    
    # ==================== СИНТАКСИЧЕСКИЕ ОШИБКИ ====================
    "40. ОШИБКА: нет точки с запятой": """
        int x = 10
        int y = 20;
    """,
    
    "41. ОШИБКА: пропущен идентификатор": """
        int = 5;
    """,
    
    "42. ОШИБКА: пропущен знак равенства": """
        int x 10;
    """,
    
    "43. ОШИБКА: лишняя точка с запятой": """
        int x = 10;;
    """,
    
    "44. ОШИБКА: отсутствие int при объявлении": """
        x = 10;
    """,
    
    "45. ОШИБКА: незакрытая скобка": """
        int x = (10 + 5;
    """,
    
    "46. ОШИБКА: лишняя закрывающая скобка": """
        int x = 10 + 5);
    """,
    
    # ==================== ЛЕКСИЧЕСКИЕ ОШИБКИ ====================
    "47. ОШИБКА: неизвестный символ (@)": """
        int x = 10;
        x = x @ 5;
    """,
    
    "48. ОШИБКА: неизвестный символ (#)": """
        int x = 10;
        x = #x + 5;
    """,
    
    "49. ОШИБКА: неизвестный символ ($)": """
        int x = 10;
        x = x $ 2;
    """,
    
    "50. ОШИБКА: неизвестный символ (!)": """
        int x = 10;
        x = !x;
    """,
}


def run_test(name: str, code: str, should_fail: bool = False):
    """Функция запуска одного теста"""
    print(f"\n{'='*70}")
    print(f"ТЕСТ: {name}")
    print(f"{'='*70}")
    print("Код:")
    for i, line in enumerate(code.strip().split('\n'), 1):
        print(f"  {i:2d} | {line}")
    print()
    
    try:
        # 1. Лексический анализ
        scanner = Scanner(code)
        tokens = scanner.scan()
        
        # 2. Семантический анализатор
        analyzer = SemanticAnalyzer()
        
        # 3. Синтаксический анализ
        parser = Parser(tokens, analyzer)
        parser.parse()
        
        if should_fail:
            print("❌ ТЕСТ ПРОВАЛЕН: Ошибка ожидалась, но код выполнился успешно!")
            return False
        else:
            analyzer.print_results()
            print(" ТЕСТ ПРОЙДЕН УСПЕШНО")
            return True
            
    except (ScannerError, ParserError, SemanticError) as e:
        if should_fail:
            print(f" ТЕСТ ПРОЙДЕН: Ошибка получена корректно -> {e}")
            return True
        else:
            print(f" ТЕСТ ПРОВАЛЕН: {e}")
            return False
    except Exception as e:
        print(f" НЕИЗВЕСТНАЯ ОШИБКА: {e}")
        return False


def run_all_tests():
    """Запуск всех тестов из словаря"""
    print("\n" + "="*70)
    print(" " * 20 + "ЗАПУСК ВСЕХ ТЕСТОВ")
    print("="*70)
    
    passed = 0
    failed = 0
    total = len(TESTS)
    
    for name, code in TESTS.items():
        # Если имя содержит "ОШИБКА", ожидаем падение
        is_error_test = "ОШИБКА" in name
        
        try:
            success = run_test(name, code, should_fail=is_error_test)
            if success:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f" КРИТИЧЕСКАЯ ОШИБКА: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(" " * 25 + "ИТОГИ ТЕСТИРОВАНИЯ")
    print("="*70)
    print(f"Всего тестов: {total}")
    print(f" Пройдено: {passed}")
    print(f" Провалено: {failed}")
    print(f"Успешность: {passed/total*100:.1f}%")
    print("="*70 + "\n")


def main():
    print("\n" + "="*70)
    print(" " * 15 + "ТРАНСЛЯТОР ЯЗЫКА ПРИСВАИВАНИЙ")
    print(" " * 22 + "Корчагин А., КМБО-05-23")
    print("="*70)
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--all":
            run_all_tests()
        else:
            # Если передан просто аргумент, ищем тест по имени
            found = False
            for name, code in TESTS.items():
                if arg.lower() in name.lower():
                    is_error_test = "ОШИБКА" in name
                    run_test(name, code, should_fail=is_error_test)
                    found = True
                    break
            
            if not found:
                print(f" Тест '{arg}' не найден.")
                print("\nДоступные тесты:")
                for i, name in enumerate(TESTS.keys(), 1):
                    print(f"  {i}. {name}")
    else:
        # Интерактивное меню
        print("\nВыберите режим:")
        print("  1 — Запустить ВСЕ тесты")
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
                is_error_test = "ОШИБКА" in name
                run_test(name, TESTS[name], should_fail=is_error_test)
            except:
                print(" Неверный номер.")
        elif choice == '3':
            print("Выход.")
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()
