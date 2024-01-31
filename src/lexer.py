import os
import re

keywords = ["var", "int", "bool", "string", "println", "tuple", "if", "else", "loop", "true", "false", "fn", "return", "break", "continue", "and", "or", "not", "try", "catch", "throw"]
operators = ["+", "-", "*", "/", "=", "<", ">", "<=", ">=", "==", "!=", "|"]
logical_operators = ["and", "or", "not"]
whitespace = [" ", "\t", "\n"]
array_methods = ["length", "head", "tail", "cons"]
# TODO: Need to add support for left/right parenthesis
left_bracket  = ["(", "[", "{"]
right_barcket = [")", "]", "}"]
endofstream   = [";"]

# keyword can be termed as idnentifiers
# identifiers can't start with a number
# if the word starts with a number then it has to be a number
# if it starts with a _ then it has to be a identifier
# if it starts with a letter then it can be a keyword or an identifier or a logical operator or array methods
# DONE: if whitespace ingore it
# if operator or bracket then self explanatory
# error must be thrown if there is 

tokens = []
def lexer(code : str) -> list:
    splitted_code = code.split()
    print(splitted_code)
    if len(splitted_code) == 0:
        return
    for word in splitted_code:
        cur_pos = 0
        while(cur_pos < len(word)):
            if word in whitespace:
                continue
            elif re.match(pattern="0|[1-9][0-9]*", string=word):
                match = re.match(pattern="0|[1-9][0-9]*", string=word)
                num_value = match.group()
                print(num_value)

            else:
                pass
        
            cur_pos += 1e4



file_path = os.path.join("src", "..", "testcases", "testcase1.nova")
with open(file_path, "r") as code:
    for line in code:
        lexer(line)
    