class ASTNodeMeta(type):
    def __new__(cls, name, bases, dct):
        if name != 'ASTNode':
            def repr_func(self):
                return name
            dct['__repr__'] = repr_func
        return super().__new__(cls, name, bases, dct)

class ASTNode(metaclass=ASTNodeMeta):
    """Abstract b"""
    pass

class initialize(ASTNode):
    def __init__(self, values):
        self.children = []
        for i, value in enumerate(values):
            self.children.append(value)

class Start(initialize):
    def __init__(self, values):
        super().__init__(values)

class Statement(initialize):
    def __init__(self, values):
        super().__init__(values)

class VariableDeclarationInitialization(initialize):
    def __init__(self, values):
        super().__init__(values)

###########################################
##################UPDATES##################
###########################################
class VariableDeclaration(initialize):
    def __init__(self, values):
        super().__init__(values)

class VariableInitialization(initialize):
    def __init__(self, values):
        super().__init__(values)
###########################################
################ENDofUPDATES###############
###########################################

class FunctionCall(initialize):
    def __init__(self, values):
        super().__init__(values)

class FunctionDeclaration(initialize):
    def __init__(self, values):
        super().__init__(values)

class ConditionalStatement(initialize):
    def __init__(self, values):
        super().__init__(values)

class ReturnStatement(initialize):
    def __init__(self, values):
        super().__init__(values)

class LoopStatement(initialize):
    def __init__(self, values):
        super().__init__(values)

class LoopControlStatement(initialize):
    def __init__(self, values):
        super().__init__(values)

class ArrayDeclaration(initialize):
    def __init__(self, values):
        super().__init__(values)

class TupleDeclaration(initialize):
    def __init__(self, values):
        super().__init__(values)

class ArrayOperation(initialize):
    def __init__(self, values):
        super().__init__(values)

class TryCatchStatement(initialize):
    def __init__(self, values):
        super().__init__(values)

class ThrowStatement(initialize):
    def __init__(self, values):
        super().__init__(values)

class PrintStatement(initialize):
    def __init__(self, values):
        super().__init__(values)

class CatchBlock(initialize):
    def __init__(self, values):
        super().__init__(values)

class ErrorType(initialize):
    def __init__(self, values):
        super().__init__(values)

class ExpressionList(initialize):
    def __init__(self, values):
        super().__init__(values)

class ParameterList(initialize):
    def __init__(self, values):
        super().__init__(values)

class AssignedValue(initialize):
    def __init__(self, values):
        super().__init__(values)

class ExpressionList(initialize):
    def __init__(self, values):
        super().__init__(values)

class Expression(initialize):
    def __init__(self, values):
        super().__init__(values)

class Condition(initialize):
    def __init__(self, values):
        super().__init__(values)

class Condition1(initialize):
    def __init__(self, values):
        super().__init__(values)
class Condition2(initialize):
    def __init__(self, values):
        super().__init__(values)

class Condition3(initialize):
    def __init__(self, values):
        super().__init__(values)

class ArithmeticOperators(initialize):
    def __init__(self, values):
        super().__init__(values)

class AddOperand(initialize):
    def __init__(self, values):
        super().__init__(values)

class MulOperand(initialize):
    def __init__(self, values):
        super().__init__(values)

class TerminalOperand(initialize):
    def __init__(self, values):
        super().__init__(values)

class Literal(initialize):
    def __init__(self, values):
        super().__init__(values)







# <-----------------------------------Data Types------------------------------------>

class int(initialize):
    def __init__(self, value):
        self.value = value
        print(self.value)

class string(initialize):
    def __init__(self, value):
        self.value = value
        print(self.value)

class bool(initialize):
    def __init__(self, value):
        self.value = value
        print(self.value)

# <-----------------------------------Type Classes------------------------------------>
class base_object_class:
    def _repr_(self):
        return self._class.name_

class Number(base_object_class):
    def _init_(self):
        pass 