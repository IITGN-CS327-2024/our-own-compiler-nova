import def_node_classes
import lark


class symbolTable:
    def __init__(self):
        # The inner list would contain the data of the current scope
        self.symbol_table = [[]]

    def lookup_all_prev_scopes(self, token, type=None):
        last_index = len(self.symbol_table) - 1
        # Iterating from the last (innermost) scope to the first (outermost) scope
        for i in range(last_index, -1, -1):
            # Check each entry in the current scope
            for entry in self.symbol_table[i]:
                if 'token' in entry and entry['token'].value == token:  # Safely access 'token'
                    return entry
        return None
    
    def lookup_prev_func_scope(self, token, type='function'):
        second_last_index = len(self.symbol_table) - 2
        for i in range(second_last_index, -1, -1):
            for entry in self.symbol_table[i]:
                if entry['type'] == type:

                    # Now, need to loop over the parameters of the function
                    for i in range(len(entry['parameters'])):
                        if entry['parameters'][i] == token:
                            return entry, i
                        
        return None, 0
                    

    # TODO: Need to change it
    # The last entry in the symbol table would be the current scope
    def lookup_current_scope(self, token, type=None):
        last_index = len(self.symbol_table) - 1
        if type == None:
            for data in self.symbol_table[last_index]:
                if data['token'] == token:
                    return data
            return None
        elif type == 'Function':
            for data in self.symbol_table[last_index]:
                if data['type'] == type:
                    for i in range(len(data['parameters'])):
                        if data['parameters'][i] == token:
                            return data, i
            return None

    def incremnet_scope(self):
        self.symbol_table.append([])

    def decrement_scope(self):
        self.symbol_table.pop()

    def insert(self, data):
        last_index = len(self.symbol_table) - 1
        self.symbol_table[last_index].append(data)


'''
    Based on the type of the node we need to visit it according in the ast.
    nodeVisitor would dynamically determine which method to call in the
    sementicAnalyzer class. It would be used to traverse the ast recursively.
'''
class nodeVisitor:
    def visit(self, node):
        # mehtod_name would contain the name of the method to be called
        # e.g., visit_variable_declaration_initialization, visit_function_call, etc
        method_name = f'node_{node.__class__.__name__}'
        # Assigning the appropriate method to be called, if not found then generic_visit
        visitor = getattr(self, method_name, self.generic_visit)
        # calls the required method on the node in the sementicAnalyzer class and
        # returns the result. If the method is not found then it would call the generic_visit method
        # print("method name:", method_name)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(
            f'No node_{node.__class__.__name__} method found in sementicAnalyzer')

class codeGenerator(nodeVisitor):
    def __init__(self) -> None:
        self.symbol_table = symbolTable()
        self.final_str = ''

    def node_Start(self, node):
        for child in node.children:
            self.visit(child)

        with open('../generated_code/code_output.c', 'w') as f:
            f.write(self.final_str)

    def node_Statement(self, node):
        
        return_value = None
        for child in node.children:
            return_value = return_value or self.visit(child)
        return return_value

    def node_VariableDeclarationInitialization(self, node):
        '''
            Structure in AST: ['datatype', 'identifier', '=', 'value']
        '''
    

    # PrintStatement can print datatypes of the type NUMBER, STRING, and BOOLEAN
    # declared variables and return values of functions
    def node_PrintStatement(self, node):
        '''
            Structure in AST: ['print', 'value_to_be_printed']
            It can print the values of the type NUMBER, STRING, and BOOLEAN
            declared variables and return values of functions
        '''


    def node_FunctionDeclaration(self, node):
        '''
            Structure in AST: ['fn', 'function_name', '(', 'parameter_list', ')', 'function_body']
        '''
        function_name = node.children[1]
        return_type = node.children[-2]
        self.final_str += f'{return_type} {function_name} ('
        
        # Filling up the parameters of the function
        stop = len(node.children) - 3
        for i in range(2, stop, 2):
            parameter_type = node.children[i]
            parameter = node.children[i + 1]
            if i == stop - 1:
                self.final_str += f'{parameter_type} {parameter}'
            else:   
                self.final_str += f'{parameter_type} {parameter},'
        self.final_str += ')\n'
        self.final_str += '{\n'

        # Visiting the function body
        fn_body = self.visit(node.children[-1])

        self.final_str += fn_body + '\n'
        self.final_str += '}\n\n'

        return None
        


    def node_FunctionBody(self, node):
        '''
            Structure in AST: ['statement']
        '''
        final_structure = ''
        for child in node.children:
            final_structure += self.visit(child)
        return final_structure


    def node_FunctionCall(self, node):
        '''
            Structure in AST: ['function_name', 'expression_list']
        '''
        


    def node_ReturnStatement(self, node):
        '''
            Structure in AST: ['return', 'value']
        '''
        expression = None
        if type(node.children[1]) != lark.lexer.Token:
            expression = self.visit(node.children[1])
        else:
            expression = node.children[1].value

        return f'   return {expression};'



    def node_AddOperand(self, node):
        '''
            Structure in AST: ['value', '+', 'value']
        '''
        if type(node.children[0]) != lark.lexer.Token:
            left = self.visit(node.children[0])
        else:
            left = node.children[0].value

        if type(node.children[2]) != lark.lexer.Token:
            right = self.visit(node.children[2])
        else:
            right = node.children[2].value

        operation = node.children[1].value

        return f'{left} {operation} {right}'
    
    
    def node_MulOperand(self, node):
        '''
            Structure in AST: ['value', '+', 'value']
        '''
        if type(node.children[0]) != lark.lexer.Token:
            left = self.visit(node.children[0])
        else:
            left = node.children[0].value

        if type(node.children[2]) != lark.lexer.Token:
            right = self.visit(node.children[2])
        else:
            right = node.children[2].value

        operation = node.children[1].value

        return f'{left} {operation} {right}'
    
    def node_ModuloOperand(self, node):
        '''
            Structure in AST: ['value', '+', 'value']
        '''
        if type(node.children[0]) != lark.lexer.Token:
            left = self.visit(node.children[0])
        else:
            left = node.children[0].value

        if type(node.children[2]) != lark.lexer.Token:
            right = self.visit(node.children[2])
        else:
            right = node.children[2].value

        operation = node.children[1].value

        return f'{left} {operation} {right}'