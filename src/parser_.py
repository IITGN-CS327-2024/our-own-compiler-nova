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
from code_generation import codeGenerator


this_module = sys.modules[__name__]

# OBSERVATION: The grammar has epsilon productions due to which the AST can produce NONE as a terminal node
# TODO: array declaration without expression
# TODO: expression list
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

    

    variable_declaration: VAR DATA_TYPE IDENTIFIER END_OF_STMT

    variable_declaration_initialization: VAR DATA_TYPE IDENTIFIER ASSIGN assigned_value END_OF_STMT

    variable_initialization: IDENTIFIER ASSIGN assigned_value END_OF_STMT

    function_declaration: FN IDENTIFIER LEFT_PARENTHESIS _parameter_list RIGHT_PARENTHESIS DOUBLE_COLON DATA_TYPE function_body END_OF_STMT
                        | FN IDENTIFIER LEFT_PARENTHESIS _parameter_list RIGHT_PARENTHESIS DOUBLE_COLON VOID function_body END_OF_STMT
    function_body: LEFT_BRACES statement+ RIGHT_BRACES

    conditional_statement: IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS THEN LEFT_BRACES statement* RIGHT_BRACES END_OF_STMT ELSE THEN LEFT_BRACES statement* RIGHT_BRACES END_OF_STMT
                        | IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS THEN LEFT_BRACES statement+ RIGHT_BRACES END_OF_STMT
    
    return_statement: RETURN SEPERATOR expression END_OF_STMT

    loop_statement: LOOP THROUGH LEFT_PARENTHESIS expression RIGHT_PARENTHESIS LEFT_BRACES statement* RIGHT_BRACES END_OF_STMT

    loop_control_statement: BREAK END_OF_STMT | CONTINUE END_OF_STMT

    array_declaration: VAR DATA_TYPE ARRAY IDENTIFIER ASSIGN LEFT_BRACKET _expression_list RIGHT_BRACKET END_OF_STMT
                    |  VAR ARRAY LEFT_PARENTHESIS literal RIGHT_PARENTHESIS DATA_TYPE IDENTIFIER END_OF_STMT
    
    tuple_declaration: VAR TUPLE DATA_TYPE IDENTIFIER ASSIGN LEFT_PARENTHESIS _expression_list RIGHT_PARENTHESIS END_OF_STMT

    array_operation: IDENTIFIER ARRAY_OPERATOR ARRAY_OPERATION
                    | IDENTIFIER ARRAY_OPERATOR ARRAY_OPERATION LEFT_PARENTHESIS literal RIGHT_PARENTHESIS END_OF_STMT

    ARRAY_OPERATION: "length" | "head" | "tail" | "cons"

    try_catch_statement: TRY LEFT_BRACES statement* RIGHT_BRACES END_OF_STMT catch_block

    catch_block: CATCH LEFT_PARENTHESIS ERROR_TYPE RIGHT_PARENTHESIS LEFT_BRACES statement+ RIGHT_BRACES END_OF_STMT catch_block
                |

    throw_statement: THROW ERROR_TYPE END_OF_STMT

    ERROR_TYPE: "TypeError"
                | "DivisionByZeroError" 
                | "NameError" 
                | "IndexError" 
                | "e"


    print_statement: PRINTLN LEFT_PARENTHESIS expression RIGHT_PARENTHESIS END_OF_STMT

    _parameter_list: DATA_TYPE IDENTIFIER 
                    | DATA_TYPE IDENTIFIER SEPERATOR _parameter_list 
                    | ARRAY DATA_TYPE IDENTIFIER SEPERATOR _parameter_list
                    |
    
    assigned_value: expression 
                  | function_call
    
    function_call: IDENTIFIER LEFT_PARENTHESIS _expression_list RIGHT_PARENTHESIS
                 | IDENTIFIER LEFT_PARENTHESIS _expression_list RIGHT_PARENTHESIS END_OF_STMT

    _expression_list: expression 
                   | expression SEPERATOR _expression_list
                   |
                     
    expression: condition
                | | IDENTIFIER LEFT_BRACKET literal RIGHT_BRACKET
                | IDENTIFIER LEFT_BRACKET literal RIGHT_BRACKET END_OF_STMT
                | IDENTIFIER LEFT_BRACKET literal SEPERATOR literal RIGHT_BRACKET
                | expression STRING_OPERATOR condition
                | function_call
                | array_operation

    condition: condition AND condition1 
                | condition1
    condition1: condition1 OR condition2 
                | condition2
    condition2: NOT condition3 
                | condition3
    condition3: arithmetic_operation 
                | MINUS arithmetic_operation 
                | UNARY_NOT arithmetic_operation 
                | arithmetic_operation COMPARISON_OPERATOR arithmetic_operation

    COMPARISON_OPERATOR: ">" | "<" | ">=" | "<=" | "==" | "!="
                
    arithmetic_operation: add_operand | array_operation
    add_operand: add_operand PLUS mul_operand 
                | add_operand MINUS mul_operand 
                | mul_operand

    mul_operand: mul_operand MULTIPLY modulo_operand 
                | mul_operand DIVIDE modulo_operand 
                | modulo_operand

    modulo_operand: modulo_operand MODULO terminal_operand
                    |terminal_operand

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

    DATA_TYPE: "int" | "bool" | "string"
    VOID: "void"
    
    VAR: "var"
    PRINTLN: "println"
    ARRAY: "array"
    TUPLE: "tuple"
    IF: "if"
    ELSE: "else"
    THEN: "then"
    LOOP: "loop"
    THROUGH: "through"
    FN: "fn"
    RETURN: "return"
    TRY: "try"
    CATCH: "catch"
    THROW: "throw"
    BREAK: "break"
    CONTINUE: "continue"

    PLUS: "+"
    MINUS: "-"
    MULTIPLY: "*"
    DIVIDE: "/"
    MODULO: "%"

    COMPARE_OPERATOR: ">" | "<" | ">=" | "<=" | "==" | "!="
    AND: "and"
    OR: "or"
    NOT: "not"

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

    code_generation = codeGenerator()
    code_generation.node_Start(ast)