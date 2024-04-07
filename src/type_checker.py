import def_node_classes
import lark


class symbolTable:
    def __init__(self):
        # The inner list would contain the data of the current scope
        self.symbol_table = [[]]

    def lookup_all_prev_scopes(self, token):
        last_index = len(self.symbol_table) - 1
        # Iterating from the last scope to the first scope
        for i in range(last_index - 1, -1, -1):
            if self.symbol_table[i][0]['token'].value == token:
                return self.symbol_table[i][0]
        return None

    # TODO: Need to change it
    # The last entry in the symbol table would be the current scope
    def lookup_current_scope(self, token):
        last_index = len(self.symbol_table) - 1
        for data in self.symbol_table[last_index]:

            if data['token'] == token:
                return data
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
        method_name = f'visit_{node.__class__.__name__}'
        # Assigning the appropriate method to be called, if not found then generic_visit
        visitor = getattr(self, method_name, self.generic_visit)
        # calls the required method on the node in the sementicAnalyzer class and
        # returns the result. If the method is not found then it would call the generic_visit method
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(
            f'No visit_{node.__class__.__name__} method found in sementicAnalyzer')


class sementicAnalyzer(nodeVisitor):
    def __init__(self) -> None:
        self.symbol_table = symbolTable()

    def get_data_type(self, node):
        # print("\nget_data_type:", node.__class__.__name__)
        if isinstance(node, lark.lexer.Token):
            if node.value == 'int':
                return 'NUMBER'
            if node.value == 'string':
                return 'STRING'
            if node.value == 'bool':
                return 'BOOLEAN'
            else:
                print("here")
                raise Exception(f"Invalid data type {node}")

        elif isinstance(node, def_node_classes.int):
            print("hi")
            return def_node_classes.Number
        else:
            raise Exception(f"Invalid data type {node}")

    def visit_Start(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Statement(self, node):
        for child in node.children:
            self.visit(child)


    def visit_VariableDeclarationInitialization(self, node):
        '''
            Structure in AST: ['datatype', 'identifier', '=', 'value']
        '''
        # Need to check if the variable is already declared in the current scope
        data = self.symbol_table.lookup_current_scope(node.children[1])

        if data != None:
            raise Exception(
                f"Variable {node.children[1]} already declared in the current scope"
            )

        # Collecting the necessary information, for the symbol table
        data = {
            'type'      : 'variable',
            'token'     : node.children[1],
            'value'     : node.children[3],
            'data_type' : self.get_data_type(node.children[0])
        }

        ###############################
        ####### Check for the type######
        ###############################
        print("node.children[0]", node.children[0].value)
        print("node.children[1]", node.children[1].type)
        print("node.children[3]", node.children[3].type)
        print(type(node.children[3]))
        ''' 
            Findings:
                - all the temnials would be of the type lark.lexer.Token
                - lark.lexer.Token contains 2 attributes: type and value
                - type is the token class and value is the value of the token
        '''
        ###############################
        ###############################
        ###############################
        self.symbol_table.insert(data)
        print("\nSYMBOL TABLE:", self.symbol_table.symbol_table, "\n")

        # Need to verify the type of the assigned value with the type declaration of the variable
        assigned_value = data['value']
        if data['value'].type != data['data_type']:
            raise Exception(
                f"Type mismatch: {assigned_value} is not of type {data['data_type']}")
        else:
            return None
        

    def visit_VariableDeclaration(self, node):
        '''
            Structure in AST: ['datatype', 'identifier']
        '''
        # Need to check if the variable is already declared in the current scope
        data = self.symbol_table.lookup_current_scope(node.children[1])

        if data != None:
            raise Exception(
                f"Variable {node.children[1]} already declared in the current scope"
            )

        # Collecting the necessary information, for the symbol table
        data = {
            'type'      : 'variable',
            'token'     : node.children[1],
            'value'     : None,
            'data_type' : self.get_data_type(node.children[0])
        }
        self.symbol_table.insert(data)
        print("\nSYMBOL TABLE:", self.symbol_table.symbol_table, "\n")
        return None

    def visit_VariableInitialization(self, node):
        '''
            Structure in AST: ['identifier', '=', 'value']
        '''
        data = self.symbol_table.lookup_current_scope(node.children[0])

        if data == None:
            data = self.symbol_table.lookup_all_prev_scopes(node.children[0])
            if data == None:
                raise Exception(
                    f"Variable {node.children[0]} not declared in the current scope"
                )

        # Collecting the necessary information, for the symbol table
        data = {
            'type'      : 'variable',
            'token'     : node.children[0],
            'value'     : node.children[2],
            'data)type' : data['type']
        }
        self.symbol_table.insert(data)
        print("\nSYMBOL TABLE:", self.symbol_table.symbol_table, "\n")
        return None
    

    # PrintStatement can print datatypes of the type NUMBER, STRING, and BOOLEAN
    # declared variables and return values of functions
    def visit_PrintStatement(self, node):
        '''
            Structure in AST: ['print', 'value_to_be_printed']
        '''

        # Need to check the type of the value to be printed
        if type(node.children[1]) != lark.lexer.Token:
            value_to_print = self.visit(node.children[1])
        # IDENTIFIER in case of a variable or a function call
        elif node.children[1].type == 'IDENTIFIER':
            data = self.symbol_table.lookup_current_scope(node.children[1])
            if data == None:
                # If the variable is not declared in the current scope then need to check in the previous scopes
                # This is because, new scopes are created only when a conditional staement is encountered,
                # a function is called, or a loop is encountered. Therefore, need to take the value from there as well
                data = self.symbol_table.lookup_all_prev_scopes(node.children[1])
                if data == None:
                    raise Exception(
                        f"Variable {node.children[1]} not declared in the current scope"
                    )
            value_to_print = data['data_type']
        else:
            # Here, the parameter is a terminal
            value_to_print = node.children[1].type


        # The values that can be printed are of the type NUMBER, STRING, and BOOLEAN only
        if value_to_print != 'NUMBER' and value_to_print != 'STRING' and value_to_print != 'BOOLEAN':
            raise Exception(f"Invalid data type {value_to_print}, to print")
        return None
    

    def visit_ConditionalStatement(self, node):
        '''
            Structure in AST: ['if', 'condition', 'statemnt', 'else', 'statement']
            else block may not be present
        '''

        # Need to increment the scope
        self.symbol_table.incremnet_scope()
        print(self.symbol_table.symbol_table)

        # If it is a non-terminal node then need to recursively visit it
        if type(node.children[1]) != lark.lexer.Token:
            condition = self.visit(node.children[1])

        # IDENTIFIER in case of a variable or a function call
        elif node.children[1].type == 'IDENTIFIER':
            data = self.symbol_table.lookup_current_scope(node.children[1])
            if data == None:
                data = self.symbol_table.lookup_all_prev_scopes(node.children[1])
                if data == None:
                    raise Exception(
                        f"Variable '{node.children[1]}' is not declared"
                    )
            condition = data['data_type']

        # Here, it is checking for the simplest case i.e., NUMBERS, and BOOLEAN value
        else:
            condition = node.children[1].type

        # The condition should be of the type BOOLEAN or NUMBER after evaluating it
        if condition != 'BOOLEAN' and condition != 'NUMBER':
            raise Exception(f"Invalid data type '{condition}', for the condition")

        # Now visit the statement block
        self.visit(node.children[2])

        # If there are 5 adj_nodes then else block is present
        if (len(node.children) == 5):
            self.visit(node.children[4])

        # At the end we will exit the scope.
        # Therefore, need to decrement the scope
        self.symbol_table.decrement_scope()
        return None
