
import sys
from scanner import Scanner, ScannerError
from parser import Parser, ParserError
from semantic import SemanticAnalyzer, SemanticError

def run(source_code, source_name="input"):
    print(f"--- Компиляция программы: {source_name} ---")
    try:
        # 1. Лексический анализ
        scanner = Scanner(source_code)
        tokens = scanner.scan()
        print("[OK] Лексический анализ завершен.")
        
        # 2. Синтаксический и семантический анализ
        analyzer = SemanticAnalyzer()
        parser = Parser(tokens, analyzer)
        parser.parse_program()
        print("[OK] Синтаксический и семантический анализ завершен.")
        
        # 3. Вывод результатов
        analyzer.print_results()
        
    except ScannerError as e:
        print(f"[ERROR] Лексическая ошибка: {e}")
    except ParserError as e:
        print(f"[ERROR] Синтаксическая ошибка: {e}")
    except SemanticError as e:
        print(f"[ERROR] Семантическая ошибка: {e}")
    except Exception as e:
        print(f"[ERROR] Неизвестная ошибка: {e}")

if __name__ == "__main__":
    # Пример 1 из лабораторной работы
    example_code = """
    int x = 15;
    int y = 3;
    int result;
    result = x + y * 4;
    result = result - 5;
    """
    run(example_code, "Пример 1")

    # Пример 2 (Унарный минус и приоритет)
    example_code_2 = """
    int a = 10;
    int b = -a;
    int c = -(a + b);
    """
    run(example_code_2, "Пример 2")