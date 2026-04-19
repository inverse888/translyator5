
from enum import Enum, auto

class TokenType(Enum):
    # Ключевые слова
    INT = auto()        # int
    
    # Данные
    ID = auto()         # Имя переменной (a, b, x)
    INTLITERAL = auto() # Число (10, 45, 0)
    
    # Операторы
    PLUS = auto()       # +
    MINUS = auto()      # -
    MUL = auto()        # *
    DIV = auto()        # /
    ASSIGN = auto()     # =
    
    # Разделители
    SEMICOLON = auto()  # ;
    LPAREN = auto()     # (
    RPAREN = auto()     # )
    
    # Специальные
    EOF = auto()        # Конец файла

class Token:
    def __init__(self, type_: TokenType, value: str = None, line: int = 0, col: int = 0):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}')"