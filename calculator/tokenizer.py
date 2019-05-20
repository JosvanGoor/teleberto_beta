
# Token container
class Token:
    NUMBER = "number"
    IDENTIFIER = "identifier"
    EOL = "eol"

    PLUS = "plus"
    MINUS = "minus"
    STAR = "star"
    SLASH = "slash"
    HAT = "hat" # '^'
    LEFT_PAREN = "left_paren"
    RIGHT_PAREN = "right_paren"

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