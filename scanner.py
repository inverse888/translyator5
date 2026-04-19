
from tokens import Token, TokenType

class ScannerError(Exception):
    pass

class Scanner:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1
        self.current_char = self.text[0] if self.text else None

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            if self.text[self.pos] == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def scan_int_literal(self):
        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(TokenType.INTLITERAL, result, self.line, self.col)

    def scan_identifier(self):
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # Проверка на ключевое слово
        if result == 'int':
            return Token(TokenType.INT, result, self.line, self.col)
        return Token(TokenType.ID, result, self.line, self.col)

    def scan(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
            elif self.current_char.isdigit():
                tokens.append(self.scan_int_literal())
            elif self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.scan_identifier())
            elif self.current_char == '+':
                tokens.append(Token(TokenType.PLUS, '+', self.line, self.col))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TokenType.MINUS, '-', self.line, self.col))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TokenType.MUL, '*', self.line, self.col))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TokenType.DIV, '/', self.line, self.col))
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(TokenType.ASSIGN, '=', self.line, self.col))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(TokenType.SEMICOLON, ';', self.line, self.col))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TokenType.LPAREN, '(', self.line, self.col))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TokenType.RPAREN, ')', self.line, self.col))
                self.advance()
            else:
                raise ScannerError(f"Неизвестный символ '{self.current_char}' на строке {self.line}")
        
        tokens.append(Token(TokenType.EOF, None, self.line, self.col))
        return tokens