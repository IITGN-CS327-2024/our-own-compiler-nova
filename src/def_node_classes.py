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

class Start(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class Statement(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class VariableDeclarationInitialization(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class FunctionCall(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class FunctionDeclaration(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class ConditionalStatement(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class ReturnStatement(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class LoopStatement(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class LoopControlStatement(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class ArrayDeclaration(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class TupleDeclaration(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class ArrayOperation(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class TryCatchStatement(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class ThrowStatement(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class PrintStatement(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class CatchBlock(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class ErrorType(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class ExpressionList(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class ParameterList(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class AssignedValue(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class ExpressionList(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class Expression(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class Condition(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class Condition1(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
class Condition2(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class Condition3(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class ArithmeticOperators(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class AddOperand(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class MulOperand(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class TerminalOperand(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class Literal(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)














