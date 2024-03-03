import os
import sys
from lexer import lexer
from lark import Lark
from lark.tree import pydot__tree_to_png

grammar = """
    start: statement*

    statement: variable_declaration | variable_initialization | array_declaration | tuple_declaration | if_statement | loop_statement | print_statement | function_declaration | try_catch_statement | function_call | array_cons | flow_control_statement | throw_statement | return_statement

    variable_declaration: "var" type identifier (";" | ("=" expression ";")? | "=" function_call)
    variable_initialization: identifier "=" expression ";"
    array_declaration: "var" "array" type identifier "=" "[" expression_list "]" ";"
    tuple_declaration: "var" "tuple" type identifier "=" "(" expression_list ")" ";"
    if_statement: "if" "(" expression ")" "{" statement* "}" ";" ("else" "{" statement* "}" ";")?
    loop_statement: "loop" "(" expression ")" "{" statement* "}" ";"
    print_statement: "println" "(" expression ")" ";" 
    function_declaration: "fn" identifier "(" parameter_list ")" "::" type "{" statement* "}" ";"
    try_catch_statement: "try" "{" statement* "}" ";" catch_block+ 
    catch_block: "catch" "(" identifier ")" "{" statement* "}" ";"
    function_call: identifier "(" expression_list ")" ";"
    array_cons: identifier "." array_method ";"
    throw_statement: "throw" expression ";"
    return_statement: "return" expression ";"
    flow_control_statement: "break" ";" | "continue" ";"
    
    type: "int" | "bool" | "string" | "void"
    expression_list: expression* ("," expression)*
    expression: literal | identifier | unary_expression | binary_expression | array_access | function_call | identifier "." array_method | "("expression")" | expression "|" expression
    array_method: "length" | "head" | "tail" | "cons" "(" number ")"
    literal: number | boolean | string
    number: NUMBER
    boolean: "true" | "false"
    string: /"[^"]*"/
    identifier: /[a-zA-Z_]\w*/
    unary_expression: ("-" | "!" | "not") expression
    binary_expression: expression ("+" | "-" | "*" | "/" | "and" | "or" | ">" | "<" | ">=" | "<=" | "==" | "!=") expression
    array_access: identifier "[" expression "]" | identifier "[" NUMBER ":" NUMBER "]"
    parameter_list: (type identifier ("," type identifier)*)?

    %import common.NUMBER
    %import common.WS
    %ignore WS
"""


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
tokens = parser(tokens, file_name)
# print(tokens)



parser_ = Lark(grammar)

input_text = ""
for i in range(len(tokens)):
    input_text += tokens[i][1]
    if i != len(tokens) - 1:
        input_text += " "

def error_handler(err):
    print(err)

parse_tree = parser_.parse(input_text)
print(parse_tree)
print(parse_tree.pretty())
# print(pydot__tree_to_png(parse_tree, "parse_tree.png"))



















# import os
# import sys
# from lexer import lexer
# from lark import Lark
# from lark.tree import pydot__tree_to_png

# grammar = """
#     start: statement*

#     statement: variable_declaration | array_declaration | tuple_declaration | if_statement | loop_statement | print_statement | function_declaration | try_catch_statement | function_call

#     variable_declaration: "var" type identifier "=" expression ";" 
#     array_declaration: "var" "array" type identifier "=" "[" expression_list "]" ";"
#     tuple_declaration: "var" "tuple" type identifier "=" "(" expression_list ")" ";"
#     if_statement: "if" "(" expression ")" "{" statement* "}" ("else" "{" statement* "}")?
#     loop_statement: "loop" "(" expression ")" "{" statement* "}" 
#     print_statement: "println" "(" expression ")" ";" 
#     function_declaration: "fn" identifier "(" parameter_list ")" "::" type "{" statement* "}" ";"
#     try_catch_statement: "try" "{" statement* "}" catch_block+ 
#     catch_block: "catch" "(" identifier ")" "{" statement* "}"
#     function_call: identifier "(" expression_list ")" ";"

#     type: "int" | "bool" | "string" | "void"
#     expression_list: expression ("," expression)*
#     expression: literal | identifier | unary_expression | binary_expression | array_access | function_call | "(" expression ")"
#     literal: number | boolean | string
#     number: NUMBER
#     boolean: "true" | "false"
#     string: /"[^"]*"/
#     identifier: /[a-zA-Z_]\w*/
#     unary_expression: ("-" | "!") expression
#     binary_expression: expression ("+" | "-" | "*" | "/" | "and" | "or" | ">" | "<" | ">=" | "<=" | "==" | "!=") expression
#     array_access: identifier "[" expression "]" | identifier "[" NUMBER ":" NUMBER "]"
#     parameter_list: (type identifier ("," type identifier)*)?

#     %import common.NUMBER
#     %import common.WS
#     %ignore WS

    
# """


# def parser(tokens: list, file_name: str):
#     file_path = os.path.join("..", "testcases", f"{file_name}")
#     with open(file_path, "r") as code:
#         for line in code:
#             lexer(line, tokens)
#     return tokens


# if len(sys.argv) != 2:
#     print(f"Expected 2 argments given {len(sys.argv)} arguments") 
#     sys.exit(1)
# file_name = sys.argv[1]

# tokens = []
# tokens = parser(tokens, file_name)
# # print(tokens)



# parser_ = Lark(grammar)

# input_text = ""
# # input_text = " var int a = 5; var int b = 7;"
# for i in range(len(tokens)):
#     input_text += tokens[i][1]
#     if i != len(tokens) - 1:
#         input_text += " "

# # print(input_text)

# parse_tree = parser_.parse(input_text)
# print(parse_tree)
# print(parse_tree.pretty())
# # print(pydot__tree_to_png(parse_tree, "parse_tree.png"))