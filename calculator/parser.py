from calculator.tokenizer import Token, Tokenizer
from calculator.ast import BinaryExpr, NegateExpr, ValueExpr

class Parser:

    def __init__(self):
        self.tokens = []
        self.index = 0

    def eol(self):
        return self.index >= len(self.tokens)

    def peek(self):
        return self.tokens[self.index]

    def advance(self):
        self.index += 1
        return self.tokens[self.index - 1]

    def accept(self, type):
        if type == self.peek().type:
            self.index += 1
            return True
        return False
        
    def parse(self, tokens):
        self.tokens = tokens
        self.index = 0

        return self._expression()

    # Parsing functions
    def _expression(self):
        return self._addition()

    def _addition(self):
        lhs = self._multiplication()

        while self.peek().type == Token.PLUS or self.peek().type == Token.MINUS:
            operator = self.advance()
            rhs = self._multiplication()

            lhs = BinaryExpr(lhs, operator, rhs)

        return lhs

    def _multiplication(self):
        lhs = self._power()

        while self.peek().type == Token.STAR or self.peek().type == Token.SLASH:
            operator = self.advance()
            rhs = self._power()

            lhs = BinaryExpr(lhs, operator, rhs)
        
        return lhs

    def _power(self):
        lhs = self._unary()

        while self.accept(Token.HAT):
            lhs = BinaryExpr(lhs, Token(Token.HAT), self._power())
        
        return lhs

    def _unary(self):
        if self.peek().type == Token.MINUS:
            self.advance()
            return NegateExpr(self._unary())

        return self._primary()

    def _primary(self):
        if self.peek().type == Token.NUMBER:
            return ValueExpr(float(self.advance().literal))
        elif self.accept(Token.LEFT_PAREN):
            expr = self._expression()

            if not self.accept(Token.RIGHT_PAREN):
                raise Exception("Unexpected end of line, did you forget a closing parenthesis?")
            return expr
        else:
            raise Exception("Unexpected token type {}, expected a number or '('".format(self.peek().type))