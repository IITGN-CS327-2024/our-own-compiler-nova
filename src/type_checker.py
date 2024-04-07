import def_node_classes
import lark

# Variable and function name should not be the same

'''
    DONE:
        - Variable Declaration and Initialization
        - Variable Declaration
        - Variable Initialization
        - Print Statement
        - Conditional Statement
        - Loop Statement
        - Function Call
        - Try Catch Statement
        - Catch Block
        - Throw Statement
        - Function Declaration

    NOT_NEEDED:
        - parameter_list
        - expression_list
'''


class symbolTable:
    def __init__(self):
        # The inner list would contain the data of the current scope
        self.symbol_table = [[]]

    def lookup_all_prev_scopes(self, token):
        # last_index = len(self.symbol_table) - 1
        # # Iterating from the last scope to the first scope
        # for i in range(last_index - 1, -1, -1):
        #     if self.symbol_table[i][0]['token'].value == token:
        #         return self.symbol_table[i][0]
        # return None
        last_index = len(self.symbol_table) - 1
        # Iterating from the last (innermost) scope to the first (outermost) scope
        for i in range(last_index, -1, -1):  # Fix: include the last index as well
            # Check each entry in the current scope
            for entry in self.symbol_table[i]:
                if 'token' in entry and entry['token'].value == token:  # Safely access 'token'
                    return entry
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
        method_name = f'node_{node.__class__.__name__}'
        # Assigning the appropriate method to be called, if not found then generic_visit
        visitor = getattr(self, method_name, self.generic_visit)
        # calls the required method on the node in the sementicAnalyzer class and
        # returns the result. If the method is not found then it would call the generic_visit method
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(
            f'No node_{node.__class__.__name__} method found in sementicAnalyzer')


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
            if node.value == 'void':
                return 'VOID'
            else:
                print(node.value)
                raise Exception(f"Invalid data type {node}")

        elif isinstance(node, def_node_classes.int):
            print("hi")
            return def_node_classes.Number
        else:
            raise Exception(f"Invalid data type {node}")

    def node_Start(self, node):
        for child in node.children:
            self.visit(child)

    def node_Statement(self, node):
        for child in node.children:
            self.visit(child)


    def node_VariableDeclarationInitialization(self, node):
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
        

    def node_VariableDeclaration(self, node):
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

    def node_VariableInitialization(self, node):
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
    def node_PrintStatement(self, node):
        '''
            Structure in AST: ['print', 'value_to_be_printed']
            It can print the values of the type NUMBER, STRING, and BOOLEAN
            declared variables and return values of functions
        '''

        # Need to check the type of the value to be printed
        # if type(node.children[1]) != lark.lexer.Token:
        if node.children[1].__class__.__name__ == 'FunctionCall':
            value_to_print = self.visit(node.children[1])
            if value_to_print == None:
                raise Exception(
                    f"Function {node.children[1].children[0]} does not return any value. Return type is void."
                )
        # IDENTIFIER in case of a variable or a function call
        elif node.children[1].type == 'IDENTIFIER':
            # In case of a function body, try catch block, etc the value to be printed can be inside the currrent scope
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
    

    def node_ConditionalStatement(self, node):
        '''
            Structure in AST: ['if', 'condition', 'statemnt', 'else', 'statement']
            else block may not be present
        '''

        # Need to increment the scope
        self.symbol_table.incremnet_scope()

        # If it is a non-terminal node then need to recursively visit it
        if type(node.children[1]) != lark.lexer.Token:
            condition = self.visit(node.children[1])

        # IDENTIFIER in case of a variable or a function call
        elif node.children[1].type == 'IDENTIFIER':
            # Since, it is a part of the condition therefore, it should be outside the current scope
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
        print(self.symbol_table.symbol_table)
        self.symbol_table.decrement_scope()
        return None
    

    def node_LoopStatement(self, node):
        '''
            Structure in AST: ['loop', 'condition', 'statement']
        '''

        # Need to increment the scope
        self.symbol_table.incremnet_scope()

        print(type(node.children[1]))
        # If it is a non-terminal node then need to recursively visit it
        if type(node.children[1]) != lark.lexer.Token:
            condition = self.visit(node.children[1])

        # IDENTIFIER in case of a variable only. It can't be a function call
        elif node.children[1].type == 'IDENTIFIER':
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

        # At the end we will exit the scope.
        # Therefore, need to decrement the scope
        print(self.symbol_table.symbol_table)
        self.symbol_table.decrement_scope()
        return None


    def node_FunctionDeclaration(self, node):
        '''
            Assuming the structure of node.children for a function declaration is:
            [keyword fn, function_name, [parameter_list], return_type, function_body]
        '''
        
        # Extracting function name
        function_name_token = node.children[1]  # Assuming function name is the second child
        function_name = function_name_token.value

        # Check if the function or a variable with the same name is already declared in the current scope
        if self.symbol_table.lookup_all_prev_scopes(function_name) is not None:
            raise Exception(f"Function '{function_name}' is already declared in the current scope")

        # Extracting parameters and their types
        parameters = []
        parameters_type = []
        # Parameters and their types are among the children, starting from index 2 up to the second-to-last index
        # The last two children are return_type and function_body, respectively
        for i in range(2, len(node.children) - 3, 2):
            param_type_token = node.children[i]  # Parameter type
            param_name_token = node.children[i + 1]  # Parameter name
            param_type = self.get_data_type(param_type_token)
            param_name = param_name_token.value

            parameters.append(param_name)
            parameters_type.append(param_type)

        # Extracting return type
        return_type_token = node.children[-2]  # The second-to-last child is the return type
        return_type = self.get_data_type(return_type_token)

        # Constructing the function record for the symbol table
        function_data = {
            'type': 'function',
            'token': function_name_token,
            'parameters': parameters,
            'parameters_type': parameters_type,
            'return_type': return_type
        }

        # Inserting the function declaration into the symbol table
        self.symbol_table.insert(function_data)
        print(self.symbol_table.symbol_table)

        # Incrementing scope for the function body
        self.symbol_table.incremnet_scope()

        # Visiting the function body
        function_body = node.children[-1]  # The last child is the function body
        self.visit(function_body)

        # Exiting the function scope
        self.symbol_table.decrement_scope()


    def node_FunctionCall(self, node):
        '''
            Structure in AST: ['function_name', 'expression_list']
        '''
        
        # Check if the function is declared in any of the scopes
        data = self.symbol_table.lookup_current_scope(node.children[0])
        if data == None:
            data = self.symbol_table.lookup_all_prev_scopes(node.children[0])
            if data == None:
                raise Exception(
                    f"Function '{node.children[0]}' not declared"
                )

        # expression_list node will not appear in the ast since
        # the rule starts with an underscore in the grammar.
        num_parameters_in_function_call = len(node.children[1 : ])
        
        # Need to check if the number of parameters is equal to the number of parameters in the function declaration
        if len(data['parameters']) != num_parameters_in_function_call:
            raise Exception(
                f"Number of parameters in the function call '{node.children[0]}' is not equal to the number of parameters in the function declaration"
            )
        
        '''
            Blueprint of the record for a function_declaration:
                - 'type' : 'function',
                - 'token' : function_name,
                - 'parameters' : list of parameters,
                - 'parameters_type' : list of respective parameters type,
                - 'return_type' : return_type
        '''

        print("inside functionCall:", data)
        # Need to check the type of the parameters
        for i, parameter in enumerate(node.children[1 : ]):
            if type(parameter) != lark.lexer.Token:
                parameter_type = self.visit(parameter)
            # Here onwards all are terminals, only variable
            elif parameter.type == 'IDENTIFIER':
                data = self.symbol_table.lookup_current_scope(parameter)
                if data == None:
                    data = self.symbol_table.lookup_all_prev_scopes(parameter)
                    if data == None:
                        raise Exception(
                            f"Variable '{parameter}' not declared"
                        )
                parameter_type = data['data_type']
            # Simplest case: NUMBERS, BOOLEAN, and STRING
            else:
                parameter_type = parameter.type

            # The type should match with the type of the parameter in the function declaration
            if parameter_type != data['parameters_type'][i]:
                raise Exception(
                    f"Type mismatch in the parameter {i+1} of the function call '{node.children[0]}'"
                )
            
        # The return type of the function call would be the return type of the function declaration
        # As, the values can be stored, returned, printed, or utilized in any other way
        return data['return_type']


    def node_TryCatchStatement(self, node):
        '''
            Structure in AST: ['try', 'statement', 'catch_block']
        '''

        # Need to increment the scope
        self.symbol_table.incremnet_scope()

        # Now visit the try block
        self.visit(node.children[1])

        # Now visit the catch block
        self.visit(node.children[2])

        # At the end we will exit the scope.
        # Therefore, need to decrement the scope
        self.symbol_table.decrement_scope()
        return None
    

    def node_CatchBlock(self, node):
        '''
            Structure in AST: ['catch', 'exception', 'statement']
        '''

        print(len(node.children))
        # Need to increment the scope
        self.symbol_table.incremnet_scope()

        exception_type = node.children[1].type
        # The exception should be of the type ERROR_TYPE
        if exception_type != 'ERROR_TYPE':
            raise Exception(f"Invalid data type '{exception_type}', for the exception")

        # Now visit the statement block
        self.visit(node.children[2])

        # No more catch blocks to visit
        if node.children[3] != None:
            self.visit(node.children[3])

        # At the end we will exit the scope.
        # Therefore, need to decrement the scope
        self.symbol_table.decrement_scope()
        print(self.symbol_table.symbol_table)
        return None
    
    def node_ThrowStatement(self, node):
        '''
            Structure in AST: ['throw', 'exception']
        '''

        # Need to check the type of the exception
        if node.children[1].type != 'ERROR_TYPE':
            raise Exception(f"Invalid data type '{node.children[1].type}', for the exception")
        return None
    

    # TODO: Need to revisit it. There are some bugs
    def node_Condition(self, node):
        '''
            Structure in AST: ['value', 'operator', 'value']
        '''
        # The values that can be compared are of the type BOOLEAN only
        if type(node.children[0]) == lark.lexer.Token:
            left = node.children[0]
        else:
            left  = self.visit(node.children[0])
        if type(node.children[2]) == lark.lexer.Token:
            right = node.children[2]
        else:
            right = self.visit(node.children[2])

        print(left)
        # if left.type != "BOOLEAN" or right.type != "BOOLEAN":
        #     raise Exception(f"Type mismatch: {left.type} and {right.type}")
        # return node.children[0].type
        return None