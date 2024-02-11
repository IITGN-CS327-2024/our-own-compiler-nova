import os
import sys
from lexer import lexer

def parser(tokens: list, file_name: str):
    file_path = os.path.join("..", "testcases", f"{file_name}")
    with open(file_path, "r") as code:
        for line in code:
            lexer(line, tokens)
    return tokens


if len(sys.argv) != 2:
    print(f"Expected 2 argments given {len(sys.argv)} arguments") 
    sys.exit(1)
file_name = sys.argv[1]

tokens = []
print(parser(tokens, file_name))