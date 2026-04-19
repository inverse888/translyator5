# parser.py
# Лабораторная работа 5. Корчагин Алексей, КМБО-05-23
# Грамматика:
# <Program> ::= <StatementList>
# <StatementList> ::= <Statement> | <StatementList> <Statement>
# <Statement> ::= <Declaration> | <Assignment>
# <Declaration> ::= int ID = <Expression> ; | int ID ;
# <Assignment> ::= ID = <Expression> ;
# <Expression> ::= <Term> { (+|-) <Term> }
# <Term> ::= <Factor> { (*|/) <Factor> }
# <Factor> ::= IntLiteral | ID | ( <Expression> ) | - <Factor>

from tokens import TokenType
from semantic import SemanticAnalyzer

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens, analyzer: SemanticAnalyzer):
        self.tokens = tokens
        self.pos = 0
        self.analyzer = analyzer

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1] # EOF

    def eat(self, token_type):
        if self.current_token().type == token_type:
            self.pos += 1
        else:
            raise ParserError(f"Ожидался {token_type.name}, получен {self.current_token().type.name}")

    def parse_program(self):
        # <Program> ::= <StatementList>
        while self.current_token().type != TokenType.EOF:
            self.parse_statement()

    def parse_statement(self):
        # <Statement> ::= <Declaration> | <Assignment>
        if self.current_token().type == TokenType.INT:
            self.parse_declaration()
        elif self.current_token().type == TokenType.ID:
            self.parse_assignment()
        else:
            raise ParserError(f"Ожидался оператор, получен {self.current_token().value}")

    def parse_declaration(self):
        # <Declaration> ::= int ID = <Expression> ; | int ID ;
        self.eat(TokenType.INT)
        var_name = self.current_token().value
        self.eat(TokenType.ID)

        if self.current_token().type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            value = self.parse_expression()
            self.analyzer.declare_variable(var_name, value)
        else:
            self.analyzer.declare_variable(var_name, 0) # int x;
        
        self.eat(TokenType.SEMICOLON)

    def parse_assignment(self):
        # <Assignment> ::= ID = <Expression> ;
        var_name = self.current_token().value
        self.eat(TokenType.ID)
        self.eat(TokenType.ASSIGN)
        value = self.parse_expression()
        self.analyzer.assign_variable(var_name, value)
        self.eat(TokenType.SEMICOLON)

    def parse_expression(self):
        # <Expression> ::= <Term> { (+|-) <Term> }
        # Устранена левая рекурсия
        result = self.parse_term()
        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token().type
            self.eat(op)
            right = self.parse_term()
            if op == TokenType.PLUS:
                result += right
            else:
                result -= right
        return result

    def parse_term(self):
        # <Term> ::= <Factor> { (*|/) <Factor> }
        # Устранена левая рекурсия
        result = self.parse_factor()
        while self.current_token().type in (TokenType.MUL, TokenType.DIV):
            op = self.current_token().type
            self.eat(op)
            right = self.parse_factor()
            if op == TokenType.MUL:
                result *= right
            else:
                if right == 0:
                    raise ParserError("Деление на ноль")
                result //= right # Целочисленное деление
        return result

    def parse_factor(self):
        # <Factor> ::= IntLiteral | ID | ( <Expression> ) | - <Factor>
        token = self.current_token()

        if token.type == TokenType.INTLITERAL:
            self.eat(TokenType.INTLITERAL)
            return int(token.value)

        if token.type == TokenType.ID:
            self.eat(TokenType.ID)
            return self.analyzer.get_variable_value(token.value)

        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return result

        if token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return -self.parse_factor()

        raise ParserError(f"Неожиданный токен в выражении: {token.value}")