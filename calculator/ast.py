from calculator.tokenizer import Token
from calculator.mathhelp import sqrt
import math

# Syntax:
#   expression      -> addition ; // top lvl
#   addition        -> multiplication ( ( '+' | '-' ) multiplication )* ;
#   multiplication  -> power ( ( '*' | '/' ) power )* ;
#   power           -> unary ( '^' power )* ; // this way it binds to the right
#   unary           -> '-' unary | primary ;
#   primary         -> NUMBER | "(" expression ")" | call ;
#   call            -> KEYWORD "(" argumentlist? ")" ;
#   argumentlist    -> expression ( "," expression )* ;

#   NUMBER          -> [0-9]* ( '.' [0-9]+ )? ( ( 'e' | 'E' ) '-'? [0-9]+ )? ;
#   IDENTIFIER      -> ( '_' | ALPHA ) ( ALPHANUMERIC | '_' )* ;
#   ALPHA           -> [a-z] | [A-Z] ;
#   ALPHANUMERIC    -> ALPHA | [0-9] ;
#   KEYWORD         -> "sqrt" | "pow" | "sin" | "cos" | "tan"

class BinaryExpr:

    def __init__(self, lhs, operator, rhs):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def evaluate(self):
        if self.operator.type == Token.PLUS:
            return self.lhs.evaluate() + self.rhs.evaluate()
        if self.operator.type == Token.MINUS:
            return self.lhs.evaluate() - self.rhs.evaluate()
        if self.operator.type == Token.STAR:
            return self.lhs.evaluate() * self.rhs.evaluate()
        if self.operator.type == Token.SLASH:
            lower = self.rhs.evaluate()
            if lower == 0.0:
                return float("inf")
            return self.lhs.evaluate() / lower
        if self.operator.type == Token.HAT:
            return self.lhs.evaluate() ** self.rhs.evaluate()
        return float("nan")

class CallExpr:
    functions = \
    {
        Token.KW_SQRT : sqrt,
        Token.KW_POW : math.pow,
        Token.KW_SIN : math.sin,
        Token.KW_COS : math.cos,
        Token.KW_TAN : math.tan,
        Token.KW_LOG : math.log,
        Token.KW_LN : math.log,
        Token.KW_DEG : math.degrees,
        Token.KW_RAD : math.radians,
        Token.KW_EXP : math.exp
    }

    def __init__(self, type, arguments):
        self.type = type
        self.arguments = arguments

        if not len(self.arguments) == self.type.literal:
            raise Exception("Call to {} expects {} arguments, got {} instead.".format(self.type.type, self.type.literal, len(self.arguments)))
    
    def evaluate(self):
        results = [expr.evaluate() for expr in self.arguments]
        return self.functions[self.type.type](*results)

class NegateExpr:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self):
        return -self.expr.evaluate()

class ValueExpr:

    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value