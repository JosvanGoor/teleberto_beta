from calculator.tokenizer import Tokenizer
from calculator.parser import Parser

parser = Parser()
expr = parser.parse("sqrt(2.0) + 12")
print(expr.evaluate())