import math

# Token container
class Token:
    NUMBER      = "number"
    IDENTIFIER  = "identifier"
    EOL         = "eol"

    PLUS        = "plus"
    MINUS       = "minus"
    STAR        = "star"
    SLASH       = "slash"
    HAT         = "hat" # '^'
    LEFT_PAREN  = "left_paren"
    RIGHT_PAREN = "right_paren"
    COMMA       = "comma"

    KW_SQRT     = "kw_sqrt"
    KW_POW      = "kw_pow"
    KW_SIN      = "kw_sin"
    KW_COS      = "kw_cos"
    KW_TAN      = "kw_tan"
    KW_LOG      = "kw_log"
    KW_LN       = "kw_ln"
    KW_DEG      = "kw_deg"
    KW_RAD      = "kw_rad"
    KW_EXP      = "kw_exp"

    def __init__(self, type, literal = ""):
        self.type = type
        self.literal = literal

    def __str__(self):
        return "Token: {} / '{}'".format(self.type, self.literal)

    def __repr__(self):
        return self.__str__()

# tokenize functions
# NUMBER        = [0-9]* ( '.' [0-9]+ )? ( ( 'e' | 'E' ) '-'? [0-9]+ )? ;
# IDENTIFIER    = ( '_' | ALPHA ) ( ALPHANUMERIC | '_' )* ;
# ALPHA         = [a-z] | [A-Z] ;
# ALPHANUMERIC  = ALPHA | [0-9] ;

class Tokenizer:
    keywords = \
    {
        "sqrt" : Token(Token.KW_SQRT, 1),
        "pow" : Token(Token.KW_POW, 2),
        "sin" : Token(Token.KW_SIN, 1),
        "cos" : Token(Token.KW_COS, 1),
        "tan" : Token(Token.KW_TAN, 1),
        "log" : Token(Token.KW_LOG, 2),
        "ln" : Token(Token.KW_LN, 1),
        "deg" : Token(Token.KW_DEG, 1),
        "rad" : Token(Token.KW_RAD, 1),
        "exp" : Token(Token.KW_EXP, 1)
    }

    constants = \
    {
        "e" : Token(Token.NUMBER, str(math.e)),
        "pi" : Token(Token.NUMBER, str(math.pi))
    }

    def __init__(self):
        self.string = ""
        self.index = 0

    def eol(self):
        return self.index >= len(self.string)

    def peek(self):
        return self.string[self.index]

    def advance(self):
        self.index += 1
        return self.string[self.index - 1]

    def accept(self, char):
        if char == self.string[self.index]:
            self.index += 1
            return True
        return False

    def number(self):
        literal = ""

        # consume start of number
        while self.peek().isdigit():
            literal = literal + self.advance()

        # consume fraction
        if self.peek() == ".":
            literal = literal + self.advance()

            if not self.peek().isdigit():
                raise Exception("Expected character in range [0-9] after '.', instead got {}".format(self.peek()))

            while self.peek().isdigit():
                literal = literal + self.advance()

        #consume exponent
        if self.peek() == "e" or self.peek() == "E":
            literal = literal + self.advance()

            if self.peek() == "-":
                literal = literal + self.advance()

            if not self.peek().isdigit():
                raise Exception("Expected character in range [0-9] after exponent 'e | E', instead got {}".format(self.peek()))

            while self.peek().isdigit():
                literal = literal + self.advance()

        return Token(Token.NUMBER, literal)


    def identifier(self):
        literal = ""

        while self.peek().isdigit() or self.peek().isalpha() or self.peek() == "_":
            literal = literal + self.advance()

        if literal in self.keywords:
            return self.keywords[literal]
        if literal in self.constants:
            return self.constants[literal]
        return Token(Token.IDENTIFIER, literal)

    def tokenize(self, string):
        self.string = string + "\0"
        self.index = 0

        tokens = []

        while self.index < len(self.string):
            # skip whitespace
            if self.peek() in " \n\r\t":
                self.advance()
                continue

            # one-char tokens
            if self.accept("+"):
                tokens.append(Token(Token.PLUS))
            elif self.accept("-"):
                tokens.append(Token(Token.MINUS))
            elif self.accept("*"):
                tokens.append(Token(Token.STAR))
            elif self.accept("/"):
                tokens.append(Token(Token.SLASH))
            elif self.accept("^"):
                tokens.append(Token(Token.HAT))
            elif self.accept("("):
                tokens.append(Token(Token.LEFT_PAREN))
            elif self.accept(")"):
                tokens.append(Token(Token.RIGHT_PAREN))
            elif self.accept(","):
                tokens.append(Token(Token.COMMA))

            # multichar tokens
            elif self.peek().isdigit():
                tokens.append(self.number())
            elif self.peek().isalpha() or self.peek() == "_":
                tokens.append(self.identifier())
            

            elif self.peek() == "\0":
                break
            else:
                raise Exception("Unexpected character at index {}, '{}'".format(self.index, self.peek()))

        tokens.append(Token(Token.EOL, "\0"))
        return tokens