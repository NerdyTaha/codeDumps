from antlr4 import *
from SASLexer import SASLexer
from SASParser import SASParser

def parse_sas(code: str):
    input_stream = InputStream(code)
    lexer = SASLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = SASParser(token_stream)
    tree = parser.program()  # Start rule
    return tree

# Test
sas_code = """
data test;
    set input;
    x = y + 1;
run;
"""
tree = parse_sas(sas_code)
print(tree.toStringTree(recog=parser))
