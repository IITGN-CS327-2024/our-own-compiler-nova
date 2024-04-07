import os
import sys
import def_node_classes, AST_transformer
import networkx as nx
import matplotlib.pyplot as plt


from dataclasses import dataclass
from lark import Lark, ast_utils, Transformer, v_args, Tree
from lark.lexer import Lexer, Token
from lark.tree import pydot__tree_to_png, Meta
from lexer import lexer
from typing import List
from graphviz import Digraph
from type_checker import sementicAnalyzer


this_module = sys.modules[__name__]

# grammar = """
#     start: statement*

#     statement: variable_declaration_initialization 
#             | function_call 
#             | function_declaration 
#             | conditional_statement
#             | return_statement
#             | loop_statement
#             | loop_control_statement
#             | array_declaration
#             | tuple_declaration
#             | array_operation
#             | try_catch_statement
#             | throw_statement
#             | print_statement

#     variable_declaration_initialization: variable_structure ";"

#     variable_structure: "var" data_type identifier
#                         | "var" data_type identifier "=" assigned_value
#                         | identifier "=" assigned_value

#     function_declaration: "fn" identifier "("parameter_list")" "::" data_type "{"statement*"}" ";"


#     conditional_statement: "if" "("expression")" "{"statement*"}" ";"
#                         | "if" "("expression")" "{"statement+"}" ";" "else" "{"statement*"}" ";"
    
#     return_statement: "return" expression ";"

#     loop_statement: "loop" "(" expression ")" "{" statement* "}" ";"

#     loop_control_statement: "break" ";" | "continue" ";"

#     array_declaration: "var" "array" data_type identifier "=" "["expression_list"]" ";"
#                     |   "var" "array" "("literal")" data_type identifier ";"
    
#     tuple_declaration: "var" "tuple" data_type identifier "=" "("expression_list")" ";"

#     array_operation: identifier "." method_name

#     method_name: "length" | "head" | "tail" | "cons" "("literal")" ";"

#     try_catch_statement: "try" "{" statement* "}" ";" catch_block

#     catch_block: "catch" "(" error_type ")" "{" statement* "}" ";" catch_block
#                 | "catch" "(" "e" ")" "{" statement* "}" ";"

#     error_type: "TypeError"
#                 | "DivisionByZeroError" 
#                 | "NameError" 
#                 | "IndexError" 
#                 | identifier

#     throw_statement: "throw" error_type ";"

#     print_statement: "println" "(" expression ")" ";"

#     parameter_list: data_type identifier 
#                     | data_type identifier "," parameter_list 
#                     |
    
#     assigned_value: expression 
#                   | function_call
    
#     function_call: identifier "(" expression_list ")" (";")?

#     expression_list: expression 
#                    | expression "," expression_list
#                    |
                     
#     expression: condition
#                 | identifier "["literal"]"
#                 | identifier "["literal ":" literal"]"
#                 | expression "|" condition
#                 | function_call
#                 | array_operation

#     condition: condition "and" condition1 
#                 | condition1
#     condition1: condition1 "or" condition2 
#                 | condition2
#     condition2: "not" condition3 
#                 | condition3
#     condition3: arithmetic_operation 
#                 | "-" arithmetic_operation 
#                 | "!" arithmetic_operation 
#                 | arithmetic_operation comparison_operation arithmetic_operation

#     comparison_operation: ">" | "<" | ">=" | "<=" | "==" | "!="
                
#     arithmetic_operation: add_operand | array_operation
#     add_operand: add_operand "+" mul_operand 
#                 | add_operand "-" mul_operand 
#                 | mul_operand

#     mul_operand: mul_operand "*" terminal_operand 
#                 | mul_operand "/" terminal_operand 
#                 | terminal_operand

#     terminal_operand: literal
#                     | identifier
#                     | "("expression")"

#     literal: number
#             | boolean 
#             | string


    
#     number: NUMBER
#     boolean: "true" | "false"
#     string: /"[^"]*"/
#     data_type: "int" | "bool" | "string" | "void"
#     identifier: /[a-zA-Z][a-zA-Z0-9]*/
    

#     %import common.NUMBER
#     %import common.WS
#     %ignore WS
# """

# grammar = """
#     start: statement*

#     statement: variable_declaration_initialization

#     variable_declaration_initialization: variable_structure END_OF_STMT

#     variable_structure: KEYWORD KEYWORD IDENTIFIER

#     KEYWORD: "var" | "int" | "bool" | "string" | "void"
#     IDENTIFIER: /[a-zA-Z][a-zA-Z0-9]*/
#     END_OF_STMT: ";"
# """

# TODO: loop stm, conditional stm have the same format grammer, need to fix it          ---> DONE
# TODO: return stm, print stm have the same format grammer, need to fix it              ---> DONE
# TODO: conditional stm and catch block have the same format grammer, need to fix it    ---> DONE

# CHANGES: if-else syntax: added "then" keyword before the left braces
# CHANGES: added a seperator(:) in return statement
# CHANGES: added "through" keyword in loop statement
# CHANGES: ERROR_TYPE is treated as an identifier
# CHANGES: removed catch_block from statement and kept it part of try_catch_statement only

# OBSERVATION: The grammar has epsilon productions due to which the AST can produce NONE as a terminal node


# variable_declaration_initialization:  KEYWORD KEYWORD IDENTIFIER END_OF_STMT
#                                         | KEYWORD KEYWORD IDENTIFIER ASSIGN assigned_value END_OF_STMT
#                                         | IDENTIFIER ASSIGN assigned_value END_OF_STMT





# try_catch_statement: KEYWORD LEFT_BRACES statement* RIGHT_BRACES END_OF_STMT catch_block

# catch_block: KEYWORD LEFT_PARENTHESIS IDENTIFIER RIGHT_PARENTHESIS LEFT_BRACES statement* RIGHT_BRACES END_OF_STMT catch_block
#             |

# throw_statement: KEYWORD IDENTIFIER END_OF_STMT

grammar = """
    start: statement*

    statement: variable_declaration
            | variable_declaration_initialization
            | variable_initialization 
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

    

    variable_declaration: KEYWORD KEYWORD IDENTIFIER END_OF_STMT

    variable_declaration_initialization: KEYWORD KEYWORD IDENTIFIER ASSIGN assigned_value END_OF_STMT

    variable_initialization: IDENTIFIER ASSIGN assigned_value END_OF_STMT

    function_declaration: KEYWORD IDENTIFIER LEFT_PARENTHESIS _parameter_list RIGHT_PARENTHESIS DOUBLE_COLON KEYWORD LEFT_BRACES statement+ RIGHT_BRACES END_OF_STMT


    conditional_statement: KEYWORD LEFT_PARENTHESIS expression RIGHT_PARENTHESIS KEYWORD LEFT_BRACES statement* RIGHT_BRACES END_OF_STMT KEYWORD KEYWORD LEFT_BRACES statement* RIGHT_BRACES END_OF_STMT
                        | KEYWORD LEFT_PARENTHESIS expression RIGHT_PARENTHESIS KEYWORD LEFT_BRACES statement+ RIGHT_BRACES END_OF_STMT
    
    return_statement: KEYWORD SEPERATOR expression END_OF_STMT

    loop_statement: KEYWORD KEYWORD LEFT_PARENTHESIS expression RIGHT_PARENTHESIS LEFT_BRACES statement* RIGHT_BRACES END_OF_STMT

    loop_control_statement: KEYWORD END_OF_STMT | KEYWORD END_OF_STMT

    array_declaration: KEYWORD KEYWORD KEYWORD IDENTIFIER ASSIGN LEFT_BRACKET _expression_list RIGHT_BRACKET END_OF_STMT
                    |   KEYWORD KEYWORD LEFT_PARENTHESIS literal RIGHT_PARENTHESIS KEYWORD IDENTIFIER END_OF_STMT
    
    tuple_declaration: KEYWORD KEYWORD KEYWORD IDENTIFIER ASSIGN LEFT_PARENTHESIS _expression_list RIGHT_PARENTHESIS END_OF_STMT

    array_operation: IDENTIFIER ARRAY_OPERATOR ARRAY_OPERATION
                    | IDENTIFIER ARRAY_OPERATOR ARRAY_OPERATION LEFT_PARENTHESIS literal RIGHT_PARENTHESIS END_OF_STMT

    ARRAY_OPERATION: "length" | "head" | "tail" | "cons"

    try_catch_statement: KEYWORD LEFT_BRACES statement* RIGHT_BRACES END_OF_STMT catch_block

    catch_block: KEYWORD LEFT_PARENTHESIS ERROR_TYPE RIGHT_PARENTHESIS LEFT_BRACES statement+ RIGHT_BRACES END_OF_STMT catch_block
                |

    throw_statement: KEYWORD ERROR_TYPE END_OF_STMT

    ERROR_TYPE: "TypeError"
                | "DivisionByZeroError" 
                | "NameError" 
                | "IndexError" 
                | "e"


    print_statement: KEYWORD LEFT_PARENTHESIS expression RIGHT_PARENTHESIS END_OF_STMT

    _parameter_list: KEYWORD IDENTIFIER 
                    | KEYWORD IDENTIFIER SEPERATOR _parameter_list 
                    |
    
    assigned_value: expression 
                  | function_call
    
    function_call: IDENTIFIER LEFT_PARENTHESIS _expression_list RIGHT_PARENTHESIS
                 | IDENTIFIER LEFT_PARENTHESIS _expression_list RIGHT_PARENTHESIS END_OF_STMT

    _expression_list: expression 
                   | expression SEPERATOR _expression_list
                   |
                     
    expression: condition
                | IDENTIFIER LEFT_BRACKET literal RIGHT_BRACKET
                | IDENTIFIER LEFT_BRACKET literal SEPERATOR literal RIGHT_BRACKET
                | expression STRING_OPERATOR condition
                | function_call
                | array_operation

    condition: condition LOGICAL_OPERATOR condition1 
                | condition1
    condition1: condition1 LOGICAL_OPERATOR condition2 
                | condition2
    condition2: LOGICAL_OPERATOR condition3 
                | condition3
    condition3: arithmetic_operation 
                | ARITHMETIC_OPERATOR arithmetic_operation 
                | UNARY_NOT arithmetic_operation 
                | arithmetic_operation COMPARISON_OPERATOR arithmetic_operation

    COMPARISON_OPERATOR: ">" | "<" | ">=" | "<=" | "==" | "!="
                
    arithmetic_operation: add_operand | array_operation
    add_operand: add_operand ARITHMETIC_OPERATOR mul_operand 
                | add_operand ARITHMETIC_OPERATOR mul_operand 
                | mul_operand

    mul_operand: mul_operand ARITHMETIC_OPERATOR terminal_operand 
                | mul_operand ARITHMETIC_OPERATOR terminal_operand 
                | terminal_operand

    terminal_operand: literal
                    | IDENTIFIER
                    | LEFT_PARENTHESIS expression RIGHT_PARENTHESIS

    literal: NUMBER
            | BOOLEAN 
            | STRING


    NUMBER: /[1-9][0-9]*/
    BOOLEAN: "true" | "false"
    STRING: /"[^"]*"/
    IDENTIFIER: /[a-zA-Z][a-zA-Z0-9]*/
    KEYWORD: "var" | "int" | "bool" | "string" | "println" | "array" | "tuple" | "if" | "else" | "loop" | "fn" | "return" | "void" | "break" | "continue" | "try" | "catch" | "throw"

    ARITHMETIC_OPERATOR: "+" | "-" | "*" | "/"
    COMPARE_OPERATOR: ">" | "<" | ">=" | "<=" | "==" | "!="
    LOGICAL_OPERATOR: "and" | "or" | "not"

    LEFT_PARENTHESIS: "("
    RIGHT_PARENTHESIS: ")"
    LEFT_BRACES: "{"
    RIGHT_BRACES: "}"
    LEFT_BRACKET: "["
    RIGHT_BRACKET: "]"

    DOUBLE_COLON: "::"
    SEPERATOR: "," | ":"
    ASSIGN: "="
    ARRAY_OPERATOR: "."
    UNARY_NOT: "!"
    STRING_OPERATOR: "|"
    END_OF_STMT: ";"
"""

tokens = []
# Custom lexer class that creates a generator object for each tokens
class TypeLexer(Lexer):
    def __init__(self, lexer_conf):
        pass

    def lex(self, data):
        for i in range(len(tokens)):
            token_class = tokens[i][0]
            token_value = tokens[i][1]

            yield Token(token_class, token_value)

# Returns the tokens generated by the lexer
def generate_tokens(tokens: list, file_name: str):
    file_path = os.path.join("..", "testcases", f"{file_name}")
    with open(file_path, "r") as code:
        for line in code:
            lexer(line, tokens)
    # print(tokens)
    return tokens

def create_graph(tree, graph=None):
    if graph is None:
        graph = Digraph()

    if isinstance(tree, def_node_classes.ASTNode):
        graph.node(str(id(tree)), label=str(tree))

        #Match case for int, string, bool
        if isinstance(tree, def_node_classes.int):
            graph.node(str(id(tree)), label=str(tree.value))
        elif isinstance(tree, def_node_classes.string):
            graph.node(str(id(tree)), label=str(tree.value))
        elif isinstance(tree, def_node_classes.bool):
            graph.node(str(id(tree)), label=str(tree.value))    

        # try:
        else:
            for child in tree.children:
                if isinstance(child, def_node_classes.ASTNode):
                    graph.node(str(id(child)), label = str(child))
                    graph.edge(str(id(tree)), str(id(child)))
                    create_graph(child, graph)

                elif isinstance(child, type(None)):
                    pass

                else:
                    graph.node(str(id(child)), label=str(child))
                    graph.edge(str(id(tree)), str(id(child)))
               
        # except: 
        #     pass 
        #     print("tree:", tree)
        
    return graph

def create_networkx_graph(node, graph=None):
    if graph is None:
        graph = nx.DiGraph()

    if isinstance(node, def_node_classes.ASTNode):
        graph.add_node(node)

        for child in node.children:
            if isinstance(child, def_node_classes.ASTNode):
                graph.add_node(child)
                graph.add_edge(node, child)
                create_networkx_graph(child, graph)
            elif isinstance(child, type(None)):
                pass
            else:
                graph.add_node(child)
                graph.add_edge(node, child)

    return graph

    # if graph is None:
    #     graph = Digraph()

    # if isinstance(tree, def_node_classes.ASTNode):
    #     try:
    #     children = tree.children
    #     # print(children)
    #     for child in children:
    #         # print(child)
    #         if isinstance(child, def_node_classes.ASTNode):
    #             graph.node(str(id(child)), label = str(child), filled='true')
    #             graph.edge(str(id(tree)), str(id(child)))
    #             create_graph(child, graph)

    #         else:
    #             graph.node(str(id(child)), label=str(child), shape='box', filled='true')
    #             graph.edge(str(id(tree)), str(id(child)))
    # return graph



if __name__ == "__main__":
    # Checking inputs from the user and passing it to the parser
    if len(sys.argv) != 2:
        print(f"Expected 2 argments given {len(sys.argv)} arguments") 
        sys.exit(1)
    file_name = sys.argv[1]

    # Generating the tokens using lexer and setting up the parser to use custom lexer's output
    tokens = generate_tokens(tokens, file_name)
    parser = Lark(grammar, strict=True, lexer=TypeLexer, start="start")

    with open(f"../testcases/{file_name}", "r") as code:
        source_code = code.read()

    # Generating the parse tree
    parse_tree = parser.parse(source_code)
    # print(parse_tree)
    # print(parse_tree.pretty())
    # pydot__tree_to_png(parse_tree, "parse_tree.png")
    # print("Parse tree generated successfully, check parse_tree.png file for the parse tree.")

    # Building the AST
    transformer = AST_transformer.CustomTransformer()
    ast = transformer.transform(parse_tree)

    # graph = create_networkx_graph(ast)
    # nx.draw(graph, with_labels=True)
    # plt.show()

    # print(type(ast.label))    
    # for attr, value in vars(ast).items():
    #     print(f"{attr}: {value}")

    graph = create_graph(ast)
    graph.render('AST', format='png', view=True)

    sementic_analyzer = sementicAnalyzer()
    sementic_analyzer.node_Start(ast)