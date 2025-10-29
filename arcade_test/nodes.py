import copy
import enum
import math

class Node:

    def __init__(self): self.parent = None

    def __str__(self): return 'node'

    def print_tree(self): print(f'[{self}]')

    def __copy__(self): return copy.deepcopy(self)

    def __eq__(self, other):
        if type(self) != type(other): return False
        return self._equals(other)
    
    def _equals(self, other):
        raise NotImplementedError
    
    def replace(self, new):
        if self.parent is not None:
            for i, oper in enumerate(self.parent.operands):
                if oper is self: 
                    self.parent.operands[i] = new
                    new.parent = self.parent

#####################################################################################

class Value(Node):
    def __init__(self, value):
        self.value = value
        super().__init__()

    def __str__(self): return 'value'
    
    def __len__(self): return 1

    def _equals(self, other):
        return self.value == other.value
    
    def __ne__(self, other): 
        return not self == other

class Number(Value):
    def __init__(self, value: float):
        super().__init__(value)
            
    def __str__(self):
        value = round(self.value, 4)
        if value.is_integer():
            return str(int(value))
        else: return str(value)
    
    def __len__(self): return len(str(self.value))

    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
        return NotImplemented

    def __neg__(self): return Number(-self.value)

    def __sub__(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)
        return NotImplemented

    def __pow__(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value)
        return NotImplemented
    
    def __float__(self): return float(self.value)

    def __int__(self): return int(self.value)

    def __gt__(self, other):    # >
        if isinstance(other, Number):
            return self.value > other.value
        elif isinstance(other, (int, float)):
            return self.value > other
        return NotImplemented
        
    def __lt__(self, other):    # <
        if isinstance(other, Number):
            return self.value < other.value
        elif isinstance(other, (int, float)):
            return self.value < other
        return NotImplemented
    
    def __ge__(self, other):    # >=
        if isinstance(other, Number):
            return self.value >= other.value
        elif isinstance(other, (int, float)):
            return self.value >= other
        return NotImplemented
    
    def __le__(self, other):    # <=
        if isinstance(other, Number):
            return self.value <= other.value
        elif isinstance(other, (int, float)):
            return self.value <= other
        return NotImplemented

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

class Associativity(enum.Enum):
    NONE = 0
    LEFT = -1      
    RIGHT = 1
    BOTH = 2 

#######################################

class Operator(Node):
    fixity = Fixity.INFIX
    arity = 2
    priority = 1
    associativity = Associativity.NONE
    commutativity = False

    def __init__(self, *operands: Node):
        self.operands = list(operands)
        for node in self.operands:
            node.parent = self
        super().__init__()

    @property
    def fixity(self) -> Fixity: return self.__class__.priority

    @property
    def arity(self) -> int:
        if self.__class__.arity is None: return len(self.operands)
        else: return self.__class__.arity

    @property
    def priority(self) -> int: return self.__class__.priority

    @property
    def associativity(self) -> Associativity: return self.__class__.associativity

    @property
    def commutativity(self) -> bool: self.__class__.commutativity
     
    @property
    def one(self) -> Node: return self.operands[0]

    @one.setter  
    def one(self, value: Node):
        self.operands[0] = value
        value.parent = self
        
    @property
    def two(self) -> Node: return self.operands[1]

    @two.setter
    def two(self, value: Node):
        self.operands[1] = value
        value.parent = self

    def __str__(self): return 'operator'

    def _equals(self, other):
        if len(self.operands) != len(other.operands):
            return False
        return all(a == b for a, b in zip(self.operands, other.operands))

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

    def is_child(self, node: Node):
        return any(n is node for n in self.operands)
    
    def is_descendant(self, node: Node):
        return (self is node or 
            any(isinstance(n, Operator) and n.is_descendant(node) 
                for n in self.operands))

    def result(self) -> Value: return None

    def work(self):
        if (result := self.result()) not in (None, NotImplemented):
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

class Associative:
    def work(self):
        def do_work(operator: Operator):
            if (result := operator.result()) not in (None, NotImplemented):
                operator.replace(result)
        do_work(self.associative())

    def left_associative(self) -> Operator:
        """a ∘ (b ∘ c) → (a ∘ b) ∘ c - возвращает self.one"""
        current = self
        while isinstance(current.two, self.__class__):
            current.one = self.__class__(current.one, current.two.one)
            current.two = current.two.two
            current = current.one
        return current
                
    def right_associative(self) -> Operator:
        """(a ∘ b) ∘ c → a ∘ (b ∘ c) - возвращает self.two"""
        current = self
        while isinstance(current.one, self.__class__):
            current.two = self.__class__(current.one.two, current.two)
            current.one = current.one.one
            current = current.two
        return current  

    def associative(self) -> Operator:
        result = self
        result = result.left_associative() if result.associativity in (Associativity.BOTH, Associativity.LEFT) else result
        result = result.right_associative() if result.associativity in (Associativity.BOTH, Associativity.RIGHT) else result
        return result
        
    def to_list(self):
        operands = []
        def collect(node):
            if isinstance(node, self.__class__):
                for op in node.operands:
                    collect(op)
            else: operands.append(node)
        collect(self)
        return operands

    def from_list(self, operands):
        if not operands: return self.neutral_element
        result = operands[0]
        for op in operands[1:]: 
            result = self.__class__(result, op)
        return result

class Commutative:
    def commutative(self):
        """a ∘ b → b ∘ a - поменять операнды местами"""
        if all(isinstance(oper, Value) for oper in self.operands):
            self.one, self.two = self.two, self.one

class AssociativeCommutative(Associative, Commutative):
    def commutative(self):
        def do_commutative(operator: Operator):
            operator.one, operator.two = operator.two, operator.one
        do_commutative(self.associative())

class Distributive:
    distributive_over = [] # классы над которыми дистрибутивен

    def find_root_subtree(self, node: Node):
        while node.parent.__class__ in self.__class__.distributive_over:
            node = node.parent
        return node

#####################################################################################

class Plus(AssociativeCommutative, Operator):
    fixity = Fixity.INFIX 
    arity = 2             
    priority = 5
    associativity = Associativity.BOTH
    commutativity = True 

    def __init__(self, addend1, addend2): super().__init__(addend1, addend2)
        
    def __str__(self):
        return '+'

    def result(self) -> Value:
        try:
            return self.one + self.two
        except Exception:
            return None
        
class BinaryMinus(Associative, Operator):
    fixity = Fixity.INFIX 
    arity = 2            
    priority = 5
    associativity = Associativity.LEFT
    commutativity = False 

    def __init__(self, minuend, subtrahend): super().__init__(minuend, subtrahend)

    def __str__(self): return '-'

    def result(self):
        try:
            return self.one - self.two
        except Exception: 
            return None

class Mult(AssociativeCommutative, Operator):
    fixity = Fixity.INFIX             
    arity = 2                          
    priority = 4
    associativity = Associativity.BOTH
    commutativity = True              

    def __init__(self, factor1, factor2): super().__init__(factor1, factor2)

    def __str__(self): return '*'

    def result(self) -> Value:
        try:
            return self.one * self.two
        except Exception:
            return None

class Div(Associative, Operator):
    fixity = Fixity.INFIX 
    arity = 2             
    priority = 4
    associativity = Associativity.LEFT
    commutativity = False 

    def __init__(self, dividend, divisor): super().__init__(dividend, divisor)

    def __str__(self): return '/'

    def result(self) -> Value:
        if self.one == self.two: return Number(1)
        if isinstance(self.two, Number) and self.two.value == 1: return self.one
        try:
            return self.one / self.two
        except Exception:
            return None
                   
class Pow(Associative, Operator):
    fixity = Fixity.INFIX 
    arity = 2             
    priority = 2
    associativity = Associativity.RIGHT
    commutativity = False
    
    def __init__(self, base, degree): super().__init__(base, degree)

    def __str__(self): return '^'

    def result(self) -> Value:
        try:
            return self.one ** self.two
        except Exception:
            return None
        
class UnaryMinus(Operator):
    fixity = Fixity.PREFIX
    arity = 1
    priority = 3
    associativity = Associativity.NONE 
    commutativity = False              

    def __init__(self, operand): super().__init__(operand)

    def __str__(self): return '-'

    def result(self) -> Value:
        try:
            return -self.one
        except Exception:
            return None

class Sin(Operator):
    fixity = Fixity.PREFIX
    arity = 1
    priority = 1   
    associativity = Associativity.NONE 
    commutativity = False                                   

    def __int__(self, x):
        super().__init__(x)

    def __str__(self): return 'sin'

    def result(self) -> Value:
        try:
            return Number(math.sin(self.one))
        except Exception:
            return None
        
class Cos(Operator):
    fixity = Fixity.PREFIX
    arity = 1
    priority = 1  
    associativity = Associativity.NONE 
    commutativity = False                                    

    def __init__(self, x):
        super().__int__(x)

    def __str__(self): return 'cos'

    def result(self):
        try:
            return Number(math.cos(self.one))
        except Exception:
            return None
        
class Log(Operator):
    fixity = Fixity.PREFIX
    arity = 2                          
    priority = 1                       
    associativity = Associativity.NONE 
    commutativity = False              

    def __init__(self, base, x):
        if isinstance(base, Number):
            if base <= 0 or base == 1: raise ValueError(f'основание логарифма: {base}')
        super().__init__(base, x)

    def __str__(self): return 'log'

    def result(self):
        try:
            return Number(math.log(self.two, self.one))
        except Exception:
            return None
        
class Lg(Log):
    fixity = Fixity.PREFIX
    arity = 1
    priority = 1                       
    associativity = Associativity.NONE 
    commutativity = False 

    def __init__(self, x):
        super().__init__(10, x)

    def __str__(self): return 'lg'

    def result(self):
        return super().result()
    
class Ln(Log):
    fixity = Fixity.PREFIX
    arity = 1
    priority = 1                       
    associativity = Associativity.NONE 
    commutativity = False 

    def __init__(self, x):
        super().__init__(math.e, x)
    
    def __str__(self): return 'ln'

    def result(self):
        return super().result()
  
#####################################################################################        