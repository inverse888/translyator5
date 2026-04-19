class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        # Словарь переменных: имя -> значение
        self.variables = {}
        self.output_log = []

    def declare_variable(self, name: str, value: int = None):
        if name in self.variables:
            raise SemanticError(f"Переменная '{name}' уже объявлена")
        
        # Если значения нет (int x;), инициализируем 0
        val = value if value is not None else 0
        self.variables[name] = val
        self.output_log.append(f"Объявлено: {name} = {val}")

    def assign_variable(self, name: str, value: int):
        if name not in self.variables:
            raise SemanticError(f"Переменная '{name}' не объявлена")
        self.variables[name] = value
        self.output_log.append(f"Присвоено: {name} = {value}")

    def get_variable_value(self, name: str) -> int:
        if name not in self.variables:
            raise SemanticError(f"Использование необъявленной переменной '{name}'")
        return self.variables[name]

    def print_results(self):
        print("\n--- Результаты выполнения ---")
        for line in self.output_log:
            print(line)
        print("\n--- Таблица переменных ---")
        for name, val in self.variables.items():
            print(f"  {name} = {val}")
        print("---------------------------")