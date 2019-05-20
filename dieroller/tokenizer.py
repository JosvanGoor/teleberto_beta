
class Token:
    TOKEN_NUMBER    = "number"
    TOKEN_DIE_OP    = "die_op"
    TOKEN_MINUS     = "minus"
    TOKEN_PLUS      = "plus"
    TOKEN_EOL       = "eol"

    def __init__(self, type, literal):
        self.type = type
        self.literal = literal

def tokenize(string):
    tokens = []

    idx = 0
    while idx < len(string):
        if (string[idx] in " \r\n\t"):
            idx = idx + 1
            continue

        elif string[idx].isdigit():
            literal = ""
            while idx < len(string) and string[idx].isdigit():
                literal = literal + string[idx]
                idx = idx + 1
            tokens.append(Token(Token.TOKEN_NUMBER, literal))

        elif string[idx] == "d":
            tokens.append(Token(Token.TOKEN_DIE_OP, "d"))
            idx = idx + 1

        elif string[idx] == "+":
            tokens.append(Token(Token.TOKEN_PLUS, "+"))
            idx = idx + 1

        elif string[idx] == "-":
            tokens.append(Token(Token.TOKEN_MINUS, "-"))
            idx = idx + 1

        else:
            raise Exception("Illegal character (idx: {}, char: {})".format(idx, string[idx]))
    return tokens + [Token(Token.TOKEN_EOL, "")]