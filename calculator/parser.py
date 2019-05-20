from calculator.tokenizer import Token, Tokenizer
from calculator.ast import BinaryExpr, CallExpr, NegateExpr, ValueExpr

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
        
    def parse(self, string):
        self.tokens = Tokenizer().tokenize(string)
        self.index = 0

        expr = self._expression()
        if not self.peek().type == Token.EOL:
            raise Exception("Trailing tokens, did you add an additional space or forget an operator somewhere?")            
        return expr

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
        elif self.peek().type.startswith("kw_"):
            return self._call()
        else:
            raise Exception("Unexpected token type {}, expected a number or '('".format(self.peek().type))

    def _call(self):
        keyword = self.advance()

        if not self.accept(Token.LEFT_PAREN):
            raise Exception("Expected '(', got {} instead".format(self.peek().type))
        
        arguments = []
        if not self.peek().type == Token.RIGHT_PAREN:
            arguments.append(self._expression())

        while not self.accept(Token.RIGHT_PAREN):
            if not self.accept(Token.COMMA):
                raise Exception("Expected ',' or ')', got {} instead.".format(self.peek().type))
            arguments.append(self._expression())

        return CallExpr(keyword, arguments)