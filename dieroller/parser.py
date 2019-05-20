from dieroller.tokenizer import Token, tokenize
from dieroller.expressions import RollExpr, NegateExpr, ValueExpr, SubstractionExpr, AdditionExpr

class Parser:

    def __init__(self):
        self.tokens = []
        self.index = -1

    def peek(self):
        return self.tokens[self.index]

    def advance(self):
        self.index += 1
        return self.tokens[self.index - 1]

    def end_of_line(self):
        return self.tokens[self.index].type == Token.TOKEN_EOL

    def parse(self, string):
        self.tokens = tokenize(string)
        self.index = 0
        return self.parse_addition()

    def parse_addition(self):
        lhs = self.parse_unary()

        while self.peek().type == Token.TOKEN_MINUS or self.peek().type == Token.TOKEN_PLUS:
            operator = self.advance()
            if operator.type == Token.TOKEN_MINUS:
                lhs = SubstractionExpr(lhs, self.parse_unary())
            else:
                lhs = AdditionExpr(lhs, self.parse_unary())
        
        return lhs

    def parse_unary(self):
        if self.peek().type == Token.TOKEN_MINUS:
            self.advance()
            return NegateExpr(self.parse_unary())

        return self.parse_roll()
        

    def parse_roll(self):
        if not (self.peek().type == Token.TOKEN_NUMBER):
            raise Exception("Unexpected token type, expected {}, got {} instead @ {}.".format(Token.TOKEN_NUMBER, self.peek().type, self.index))

        times = int(self.advance().literal)
        
        # print("parse_roll, current type / literal: {} / {}".format \
        # (
        #     self.peek().type,
        #     self.peek().literal
        # ))

        if (self.peek().type == Token.TOKEN_DIE_OP):
            self.advance()
            
            if not (self.peek().type == Token.TOKEN_NUMBER):
                raise Exception("Unexpected token type, expected {}, got {} instead @ {}.".format(Token.TOKEN_NUMBER, self.peek().type, self.index))
            
            return RollExpr(times, int(self.advance().literal))
        
        return ValueExpr(times)


        