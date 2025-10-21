import copy
import enum
import math

class Node:
    def __init__(self): self.parent = None

    def __str__(self): return 'node'

    def print_tree(self): print(f'[{self}]')

    def __copy__(self): return copy.deepcopy(self)
    
    def replace(self, new):
        if self.parent is not None:
            for i, oper in enumerate(self.parent.operands):
                if oper is self: 
                    self.parent.operands[i] = new
                    new.parent = self.parent

class Value(Node):
    def __init__(self, value):
        self.value = value
        super().__init__()

    def __str__(self): return 'value'
    
    def __len__(self): return 1

class Number(Value):
    def __init__(self, value: float):
        if value.is_integer():
            super().__init__(int(value))
        else:
            super().__init__(value)

    def __str__(self): return str(self.value)
    
    def __len__(self): return len(str(self.value))

    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
        return None

    def __neg__(self): return Number(-self.value)

    def __sub__(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)
        return None

    def __mul__(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)
        return None

    def __truediv__(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)
        return None

    def __pow__(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value)
        return None

class Letter(Value):
    def __init__(self, value: str):
        if value[0].isalpha and (len(value) == 1 or value[0:].isdigit()):
            super().__init__(value)
        else: raise TypeError

    def __str__(self): return self.value

    def __len__(self): return len(self.value)

#####################################################################################

class Fixity(enum.Enum):
        PREFIX = -1
        INFIX = 0
        POSTFIX = 1

class Operator(Node):
    fixity = Fixity.PREFIX
    arity = None
    priority = None
    
    def __init__(self, *operands: Node):
        self.operands = list(operands)
        for node in self.operands:
            node.parent = self
        super().__init__()

    @property
    def fixity(self): return self.__class__.priority

    @property
    def arity(self):
        if self.__class__.arity == None: return len(self.operands)
        else: return self.__class__.arity

    @property
    def priority(self): return self.__class__.priority
     
    @property
    def one(self): return self.operands[0]
        
    @property
    def two(self): return self.operands[1]

    def __str__(self): return 'operator'

    def print_tree(self):
        def resursive_print_tree(node, is_last=True, prefix=""):
            branch = "└── " if is_last else "├── "
            print(f"{prefix}{branch}[{node}]")
        
            if isinstance(node, Value): return
                
            new_prefix = prefix + ("    " if is_last else "│   ")
            
            for i, oper in enumerate(node.operands):
                is_last_operand = (i == len(node.operands) - 1)
                resursive_print_tree(oper, is_last_operand, new_prefix)
        
        print(f"[{self}]")
        if not isinstance(self, Value):
            for i, oper in enumerate(self.operands):
                is_last_operand = (i == len(self.operands) - 1)
                resursive_print_tree(oper, is_last_operand, "")
    
    def __len__(self): return 1 

    def result(self) -> Value: return None

    def work(self):
        print('work')
        result = self.result()
        if result is not None:
            self.replace(result)

    def solve(self):
        for i, operand in enumerate(self.operands):
            if isinstance(operand, Operator):
                new_operand = operand.solve()
                if new_operand is not operand:
                    self.operands[i] = new_operand
        result = self.work()
        return result if result is not None else self
    
#######################################

class Sin(Operator):
    fixity = Fixity.PREFIX
    arity = 1
    priority = 1

    def __int__(self, x):
        super().__init__(x)

    def __str__(self): return 'sin'

    def result(self) -> Value:
        try:
            return math.sin(self.one)
        except:
            return None
        
class Cos(Operator):
    fixity = Fixity.PREFIX
    arity = 1
    priority = 1

    def __init__(self, x):
        super().__int__(x)

    def __str__(self): return 'cos'

    def result(self):
        try:
            return math.cos(self.one)
        except:
            return None
        
class Log(Operator):
    fixity = Fixity.PREFIX
    arity = 2
    priority = 1

    def __init__(self, x, base):
        super().__init__(x, base)

    def __str__(self): return 'log'

    def result(self):
        try:
            return math.log(self.one, self.two)
        except:
            return None
        
class Lg(Log):
    arity = 1

    def __init__(self, x):
        super().__init__(x, 10)

    def __str__(self): return 'lg'

    def result(self):
        return super().result()
    
class Ln(Log):
    arity = 1

    def __init__(self, x):
        super().__init__(x, math.e)
    
    def __str__(self): return 'ln'

    def result(self):
        return super().result()

class Pow(Operator):
    fixity = Fixity.INFIX
    arity = 2
    priority = 2
    
    def __init__(self, base, degree): super().__init__(base, degree)

    def __str__(self): return '^'

    def result(self) -> Value:
        try:
            return self.one ** self.two
        except:
            return None

class UnaryMinus(Operator):
    fixity = Fixity.PREFIX
    arity = 1
    priority = 3

    def __init__(self, operand): super().__init__(operand)

    def __str__(self): return '-'

    def result(self) -> Value:
        try:
            return -self.one
        except:
            return None
               
class Mult(Operator):
    fixity = Fixity.INFIX
    arity = 2
    priority = 4

    def __init__(self, factor1, factor2): super().__init__(factor1, factor2)

    def __str__(self): return '*'

    def result(self) -> Value:
        try:
            return self.one * self.two
        except:
            return None

class Div(Operator):
    fixity = Fixity.INFIX
    arity = 2
    priority = 4

    def __init__(self, dividend, divisor): super().__init__(dividend, divisor)

    def __str__(self): return '/'

    def result(self) -> Value:
        try:
            return self.one / self.two
        except:
            return None
        
class BinaryMinus(Operator):
    fixity = Fixity.INFIX
    arity = 2
    priority = 5

    def __init__(self, minuend, subtrahend): super().__init__(minuend, subtrahend)

    def __str__(self): return '-'

    def result(self):
        try:
            return self.one - self.two
        except: 
            return None
                
class Plus(Operator):
    fixity = Fixity.INFIX
    arity = 2
    priority = 5

    def __init__(self, addend1, addend2): super().__init__(addend1, addend2)
        
    def __str__(self):
        return '+'

    def result(self) -> Value:
        try:
            return self.one + self.two
        except:
            return None
        
#####################################################################################        