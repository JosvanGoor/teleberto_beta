from random import randint

# Syntax:
#   command -> addition EOL ;
#
#   roll    -> NUMBER ( DIE_OP NUMBER )? ;             
#   unary   -> MINUS? (unary | roll);
#   addition-> addition ( (PLUS | MINUS) addition)* | unary ; 
#   
#   NUMBER  -> DIGIT+ ;
#   DIGIT   -> '0' ... '9' ;
#   DIE_OP  -> 'd' ;
#   MINUS   -> '-' ;
#   PLUS    -> '+' ;

class RollExpr:

    def __init__(self, times, die):
        self.times = times
        self.die = die

    def evaluate(self):
        self.value = 0

        for _ in range(0, self.times):
            self.value += randint(1, self.die)

        return self.value

    def verbose(self):
        value = 0
        values = []
        for _ in range(0, self.times):
            roll = randint(1, self.die)
            value += roll
            values.append(str(roll))

        return "( {}d{} [{}] -> {})".format(self.times, self.die, ", ".join(values), value), value

    def stringify(self):
        return self.verbose()

class NegateExpr:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self):
        return -self.expr.evaluate()

    def stringify(self):
        str, val = self.expr.stringify()
        return "( [-[{}]] -> {} )".format(str, -val), -val

class ValueExpr:

    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def stringify(self):
        return "{}".format(self.value), self.value

class AdditionExpr:

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self):
        return self.lhs.evaluate() + self.rhs.evaluate()

    def stringify(self):
        lstr, lval = self.lhs.stringify()
        rstr, rval = self.rhs.stringify()
        result = lval + rval
        return "( [{} + {}] -> {} )".format(lstr, rstr, result), result

class SubstractionExpr:

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self):
        return self.lhs.evaluate() - self.rhs.evaluate()

    def stringify(self):
        lstr, lval = self.lhs.stringify()
        rstr, rval = self.rhs.stringify()
        result = lval - rval
        return "( [{} - {}] -> {} )".format(lstr, rstr, result), result