from calculator.tokenizer import Token

# Syntax:
#   expression      -> addition ; // top lvl
#   addition        -> multiplication ( ( '+' | '-' ) multiplication )* ;
#   multiplication  -> power ( ( '*' | '/' ) power )* ;
#   power           -> unary ( '^' power )* ; // this way it binds to the right
#   unary           -> '-' unary | primary ;
#   primary         -> NUMBER | "(" expression ")" ;

#   NUMBER          -> [0-9]* ( '.' [0-9]+ )? ( ( 'e' | 'E' ) '-'? [0-9]+ )? ;
#   IDENTIFIER      -> ( '_' | ALPHA ) ( ALPHANUMERIC | '_' )* ;
#   ALPHA           -> [a-z] | [A-Z] ;
#   ALPHANUMERIC    -> ALPHA | [0-9] ;

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
            return self.lhs.evaluate() / self.rhs.evaluate()
        if self.operator.type == Token.HAT:
            return self.lhs.evaluate() ** self.rhs.evaluate()
        return float("nan")

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