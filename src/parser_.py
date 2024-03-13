import os
import sys
from lexer import lexer
from lark import Lark
from lark.tree import pydot__tree_to_png

grammar = """
    start: statement*

    statement: variable_declaration_initialization 
            | function_call 
            | function_declaration 
            | conditional_statement
            | return_statement
            | loop_statement
            | loop_control_statement
            | array_declaration
            | tuple_declaration
            | array_operation
            | try_catch_statement
            | throw_statement
            | print_statement

    variable_declaration_initialization: variable_structure ";"

    variable_structure: "var" data_type identifier
                        | "var" data_type identifier "=" assigned_value
                        | identifier "=" assigned_value

    function_declaration: "fn" identifier "("parameter_list")" "::" data_type "{"statement*"}" ";"


    conditional_statement: "if" "("expression")" "{"statement*"}" ";"
                        | "if" "("expression")" "{"statement+"}" ";" "else" "{"statement*"}" ";"
    
    return_statement: "return" expression ";"

    loop_statement: "loop" "(" expression ")" "{" statement* "}" ";"

    loop_control_statement: "break" ";" | "continue" ";"

    array_declaration: "var" "array" data_type identifier "=" "["expression_list"]" ";"
                    |   "var" "array" "("literal")" data_type identifier ";"
    
    tuple_declaration: "var" "tuple" data_type identifier "=" "("expression_list")" ";"

    array_operation: identifier "." method_name

    method_name: "length" | "head" | "tail" | "cons" "("literal")" ";"

    try_catch_statement: "try" "{" statement* "}" ";" catch_block

    catch_block: "catch" "(" error_type ")" "{" statement* "}" ";" catch_block
                | "catch" "(" "e" ")" "{" statement* "}" ";"

    error_type: "TypeError"
                | "DivisionByZeroError" 
                | "NameError" 
                | "IndexError" 
                | identifier

    throw_statement: "throw" error_type ";"

    print_statement: "println" "(" expression ")" ";"

    parameter_list: data_type identifier 
                    | data_type identifier "," parameter_list 
                    |
    
    assigned_value: expression 
                  | function_call
    
    function_call: identifier "(" expression_list ")" (";")?

    expression_list: expression 
                   | expression "," expression_list
                   |
                     
    expression: condition
                | identifier "["literal"]"
                | identifier "["literal ":" literal"]"
                | expression "|" condition
                | function_call
                | array_operation

    condition: condition "and" condition1 
                | condition1
    condition1: condition1 "or" condition2 
                | condition2
    condition2: "not" condition3 
                | condition3
    condition3: arithmetic_operation 
                | "-" arithmetic_operation 
                | "!" arithmetic_operation 
                | arithmetic_operation comparison_operation arithmetic_operation

    comparison_operation: ">" | "<" | ">=" | "<=" | "==" | "!="
                
    arithmetic_operation: add_operand | array_operation
    add_operand: add_operand "+" mul_operand 
                | add_operand "-" mul_operand 
                | mul_operand

    mul_operand: mul_operand "*" terminal_operand 
                | mul_operand "/" terminal_operand 
                | terminal_operand

    terminal_operand: literal
                    | identifier
                    | "("expression")"

    literal: number
            | boolean 
            | string


    
    number: NUMBER
    boolean: "true" | "false"
    string: /"[^"]*"/
    data_type: "int" | "bool" | "string" | "void"
    identifier: /[a-zA-Z][a-zA-Z0-9]*/
    

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