from calculator.tokenizer import Tokenizer
from calculator.parser import Parser

tokenizer = Tokenizer()

tokens = tokenizer.tokenize("10 - 3 - 2")

for token in tokens:
    print(token)

parser = Parser()
expr = parser.parse(tokens)
print(expr.evaluate())