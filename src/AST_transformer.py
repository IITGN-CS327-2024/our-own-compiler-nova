import def_node_classes
import lark

from lexer import keywords, endOfStmt
    
# Converts a list of lists to a single list
def single_list(_list):
    combined_list = []
    for entry in _list:
        if isinstance(entry, list):
            combined_list.extend(single_list(entry))
        else:
            combined_list.append(entry)
    return combined_list

def required_tokens(adj_nodes, *tokens):
    not_wanted=[]
    for token in tokens:
        not_wanted.append(token)
    not_wanted = single_list(not_wanted)
    return [tokens for tokens in adj_nodes if tokens not in not_wanted]

class CustomTransformer(lark.Transformer):

    def create_node(self, adj_nodes, node_class):
        adj_nodes = single_list(adj_nodes)
        if len(adj_nodes) == 1:
            return adj_nodes
        return node_class(adj_nodes)
    

    ################################
    ###########TERMINALS############
    ################################
    # def NUMBER(self, value):
    #     return def_node_classes.int(value)
    
    # def STRING(self, value):
    #     return def_node_classes.string(value)

    # def BOOLEAN(self, value):
    #     return def_node_classes.boolean(value)


    ################################
    #########NON-TERMINALS##########
    ################################
    def start(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        return def_node_classes.Start(adj_nodes)
    
    def statement(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        return def_node_classes.Statement(adj_nodes)
    
    def variable_declaration_initialization(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        not_required = ['var', ';']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.VariableDeclarationInitialization(adj_nodes)
    
    ##############################
    ###########UPDATES############
    ##############################
    def variable_declaration(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        not_required = ['var', ';']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.VariableDeclaration(adj_nodes)
    
    def variable_initialization(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        not_required = ['var', ';']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.VariableInitialization(adj_nodes)
    ##############################
    ########END_OF_UPDATES########
    ##############################


    def function_call(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        not_required = ['(', ',', ')', ';']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.FunctionCall(adj_nodes)
    
    def function_declaration(self, adj_nodes):
        not_required = ['(', ')', '::', ';', ',']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.FunctionDeclaration(adj_nodes)
    
    def function_body(self, adj_nodes):
        not_required = ['{', '}']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.FunctionBody(adj_nodes)
    
    def conditional_statement(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        not_required = ['then', '(', ')', '{', '}', ';']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.ConditionalStatement(adj_nodes)
    
    def return_statement(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        not_required = [':', ';']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.ReturnStatement(adj_nodes)
    
    def loop_statement(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        not_required = ['through', '(', ')', '{', '}', ';']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.LoopStatement(adj_nodes)
    
    def loop_control_statement(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        return def_node_classes.LoopControlStatement(adj_nodes)
    
    def array_declaration(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        not_required = ['var', 'array', '=', '[', ',', ']', ';', '(', ')']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.ArrayDeclaration(adj_nodes)
    
    def tuple_declaration(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        not_wanted = ['var', 'tuple', '=', '(', ',', ')', ';']
        adj_nodes = required_tokens(adj_nodes, not_wanted)
        return def_node_classes.TupleDeclaration(adj_nodes)
    
    def array_operation(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        return def_node_classes.ArrayOperation(adj_nodes)
    
    def try_catch_statement(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        not_required = ['{', '}', ';']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.TryCatchStatement(adj_nodes)
    
    def throw_statement(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        not_required = [';']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.ThrowStatement(adj_nodes)
    
    def catch_block(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        if len(adj_nodes) == 0:
            return None
        not_required = ['(', ')', '{', '}', ';']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.CatchBlock(adj_nodes)
    
    def print_statement(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        not_required = ['(', ')', ';']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.PrintStatement(adj_nodes)
    
#   <-------------------------------------------------------------------------------------------->

    def assigned_value(self, adj_nodes):
        return adj_nodes

    def expression(self, adj_nodes):
        not_required = ['[', ']', ';']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return self.create_node(adj_nodes, def_node_classes.Expression)
    
    def condition(self, adj_nodes):
        return self.create_node(adj_nodes, def_node_classes.Condition)
    
    def condition1(self, adj_nodes):
        return self.create_node(adj_nodes, def_node_classes.Condition1)

    def condition2(self, adj_nodes):
        return self.create_node(adj_nodes, def_node_classes.Condition2)
    
    def condition3(self, adj_nodes):
        return self.create_node(adj_nodes, def_node_classes.Condition3)
    
    def arithmetic_operation(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        return adj_nodes
    
    def add_operand(self, adj_nodes):
        return self.create_node(adj_nodes, def_node_classes.AddOperand)
    
    def mul_operand(self, adj_nodes):
        return self.create_node(adj_nodes, def_node_classes.MulOperand)
    
    def modulo_operand(self, adj_nodes):
        return self.create_node(adj_nodes, def_node_classes.ModuloOperand)

    def terminal_operand(self, adj_nodes):
        if len(adj_nodes) == 3:
            not_required = ['(', ')']
            adj_nodes = required_tokens(adj_nodes, not_required)
            return self.create_node(adj_nodes, def_node_classes.TerminalOperand)
        return self.create_node(adj_nodes, def_node_classes.TerminalOperand)
    
    def literal(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        return adj_nodes
    
    def expression_list(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        if len(adj_nodes) == 0:
            return None
        if len(adj_nodes) == 1:
            return adj_nodes
        not_required = [',']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.ExpressionList(adj_nodes)
    
    def parameter_list(self, adj_nodes):
        adj_nodes = single_list(adj_nodes)
        if len(adj_nodes) == 0:
            return None
        
        not_required = [',']
        adj_nodes = required_tokens(adj_nodes, not_required)
        return def_node_classes.ParameterList(adj_nodes)