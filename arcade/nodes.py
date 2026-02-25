from __future__ import annotations # это чтобы код видел типы до их объявления
from functools import cached_property # это чтобы первый раз результат свойтсва записался и не срабатывала функция каждый раз
from copy import deepcopy # для глубокого копирования
import math # функции: sin, cos, log, ...
import gc

def action(name, condition = None):
    def decorator(func):
        func.action_name = name
        func.condition = condition
        return func
    return decorator

class Node:
    ACTIONS = {}

    @property
    def actions(self) -> tuple:
        available_actions = []
        for name, func in self.__class__.ACTIONS.items():
            if func.condition is None or func.condition(self):
                available_actions.append(name)
        return tuple(available_actions)

    def do_action(self, name_action: str) -> Node: 
        func = self.__class__.ACTIONS[name_action]
        if func.condition is None or func.condition(self): return func(self)
        else: return self

    __slots__ = ['parent']

    def __init__(self): self.parent: Operator | None = None

    def __iter__(self): raise NotImplementedError()

    def __getitem__(self, key) -> Node | str: return list(iter(self))[key]

    @property
    def nodes(self) -> list[Node]: return [node for node in self if type(node) is not str]

    @property
    def values(self) -> list[Value]: return [value for value in self if isinstance(value, Value)]

    @property
    def operators(self) -> list[Operator]: 
        return [operator for operator in self if isinstance(operator, Operator)]

    def __str__(self) -> str: return 'node'

    def print_expression(self):
        result = ''
        node = self[0]
        symbol = str(node)
        result += symbol
        for node in self[1:]:
            prev_symbol = symbol
            symbol = str(node)
            if not (symbol == ')' or prev_symbol == '('): result += ' '
            result += symbol
        print(result) 
    
    def print_tree(self): print(f'[{self}]')

    def __deepcopy__(self, memo=None):
        cls = self.__class__
        result = cls.__new__(cls)
        result.parent = None
        return result

    def __eq__(self, other): return type(self) == type(other) and self._equals(other)

    def _equals(self, other): raise NotImplementedError()
    
    def replace(self, new: Node) -> Node:
        if self.parent != None:
            for i, operand in enumerate(self.parent.operands):
                if operand is self:
                    self.parent.operands[i] = new
                    new.parent = self.parent
                    self.parent = None
        else:
            for ref in gc.get_referrers(self):
                if isinstance(ref, dict):
                    for key, val in list(ref.items()):
                        if val is self:
                            ref[key] = new
            
    @action('представить как противоположный')
    def as_neg(self) -> Node: self.replace(UnaryMinus(UnaryMinus(deepcopy(self))))

    @action('представить как дробь')
    def as_fraction(self) -> Node: self.replace(Div(deepcopy(self), Number(1)))

#####################################################################################

class Value(Node):
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value
        super().__init__()

    def __str__(self) -> str: return 'value'

    def __iter__(self): yield self

    def _equals(self, other): return self.value == other.value
    
    def __hash__(self): return hash((self.__class__, self.value))
    
    def __ne__(self, other): return not self == other

    def __deepcopy__(self, memo=None):
        result = super().__deepcopy__(memo)
        result.value = deepcopy(self.value, memo)
        return result
    
class Number(Value):
    def __init__(self, value: float): super().__init__(value)

    def __str__(self) -> str:
        if self.value.is_integer(): return str(int(self.value))
        else: return str(self.value)

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

Number.ZERO = Number(0)
Number.ONE = Number(1)

class Letter(Value):
    def __init__(self, value: str):
        if value and value[0].isalpha():
            super().__init__(value)
        else: raise TypeError

    def __str__(self) -> str: return self.value

    def __add__(self, other):
        if self == other: return Mult(2, deepcopy(self))
        return NotImplemented
    
    def __sub__(self, other):
        if self == other: return Number(0)
        return NotImplemented
    
    def __mul__(self, other):
        if other == Number.ZERO: return Number(0)
        if self == other: return Pow(deepcopy(self), 2)
        return NotImplemented
    
    def __truediv__(self, other):
        if self == other: return Number(1)
        return NotImplemented

#######################################

class Operator(Node):
    ARITY = 2
    PRIORITY = 1

    __slots__ = ['operands']

    def __init__(self, *operands: Node):
        self.operands: list[Node] = list(operands)
        for node in self.operands:
            node.parent = self
        super().__init__()

    @property
    def arity(self) -> int:
        if self.__class__.Arity is None: return len(self.operands)
        else: return self.__class__.Arity

    @cached_property
    def priority(self) -> int: return self.__class__.PRIORITY
     
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
        
    def _equals(self, other):
        if len(self.operands) != len(other.operands): return False
        return all(a == b for a, b in zip(self.operands, other.operands))

    def __hash__(self):
        return hash((self.__class__,) + tuple(
            op.value if isinstance(op, Value) else op.__class__ 
            for op in self.operands))
    
    def __deepcopy__(self, memo=None):
        result = super().__deepcopy__(memo)
        result.operands = deepcopy(self.operands, memo)
        for op in result.operands:
            op.parent = result
        return result
    
    def __len__(self): return sum(1 for _ in iter(self))    

    def print_tree(self):
        def resursive_print_tree(node: Node, is_last=True, prefix=""):
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

    def is_child(self, node: Node) -> bool: return any(operand is node for operand in self.operands)
    
    def is_descendant(self, node: Node):
        return (self is node or 
            any(isinstance(n, Operator) and n.is_descendant(node) 
                for n in self.operands))

    def result(self) -> Value: raise NotImplementedError()

    @action('выполнить')
    def work(self): 
        if (result := self.result()) is not NotImplemented: self.replace(result) 

    def solve(self) -> Node:
        for i, operand in enumerate(self.operands):
            if isinstance(operand, Operator):
                new_operand = operand.solve()
                if new_operand is not operand:
                    self.operands[i] = new_operand
        result = self.work()
        return result if result != NotImplemented else self

#######################################

class Prefix:
    ARITY = 1

    def __iter__(self):
        yield self
        yield '('
        for op in self.operands: yield from op
        yield ')'

class Infix:
    ARITY = 2
    ASSOCIATIVITY_LEFT = True

    @cached_property
    def associativity_left(self) -> bool: return self.__class__.ASSOCIATIVITY_LEFT

    def needs_parentheses(self, child: Node, is_left: bool) -> bool:
        if not isinstance(child, Operator): return False
        if child.priority >= self.priority: return True
        #if child.priority == self.priority:
            #if child.__class__ != self.__class__: return True
            #return self.associativity_left != is_left
        return False

    def __iter__(self):
        left, right = self.operands
        if self.needs_parentheses(left, True):
            yield '('; yield from left; yield ')'
        else: yield from left
        yield self
        if self.needs_parentheses(right, False):
            yield '('; yield from right; yield ')'
        else: yield from right

class Postfix:
    ARITY = 1

    def __iter__(self):
        yield '('
        for op in self.operands: yield from op
        yield ')'
        yield self
        
class Associative:
    @action('ассоциативность влево')
    def associative_left(self) -> Operator:
        """a ∘ (b ∘ c) → (a ∘ b) ∘ c"""
        if isinstance(self.two, self.__class__):
            self.one = self.__class__(self.one, self.two.one)
            self.two = self.two.two
    
    @action('ассоциативность вправо')
    def associative_right(self) -> Operator:
        """(a ∘ b) ∘ c → a ∘ (b ∘ c)"""
        if isinstance(self.one, self.__class__):
            self.two = self.__class__(self.one.two, self.two)
            self.one = self.one.one
                     
    def to_list(self) -> list[Node]:
        operands = []
        def collect(n):
            if isinstance(n, self.__class__):
                for op in n.operands: collect(op)
            else: operands.append(n)
        collect(self)
        print(f"to_list: {self} -> {operands}")
        return operands
    
    @classmethod
    def from_list(cls: Infix, operands) -> Node | None:
        print(f"from_list: {operands}")
        if not operands: return None
        if len(operands) == 1: return operands[0]
        if cls.ASSOCIATIVITY_LEFT:
            result = operands[0]
            for op in operands[1:]: result = cls(result, op)
        else:
            result = operands[-1]
            for i in range(len(operands)-2, -1, -1):
                result = cls(operands[i], result)
        print(f"from_list result: {result}")
        return result
    
    def _equals(self, other) -> bool:
        self_list = self.to_list() 
        other_list = other.to_list()
        return self_list == other_list

class Commutative:
    def __hash__(self):
        return hash((self.__class__,) + tuple(sorted(
            str(op.value) if isinstance(op, Value) else op.__class__.__name__
            for op in self.operands)))
    
    def _equals(self, other) -> bool:
        return sorted(self.operands, key=hash) == sorted(other.operands, key=hash)

    @action('коммутативность')
    def commutative(self):
        """a ∘ b → b ∘ a - поменять операнды местами"""
        self.one, self.two = self.two, self.one

class Distributive:
    distributive_over: tuple[type[Associative], ...]

    def is_dist_over(self, node_cls) -> bool: return self.__class__.is_dist_over(node_cls)

    @classmethod
    def is_dist_over(cls : type, node_cls: type | Node) -> bool: 
        if node_cls is type: return node_cls in cls.distributive_over
        else: return node_cls.__class__ in cls.distributive_over

    @classmethod
    def get_max_sum(cls, operator: Operator) -> Operator:
        parent = operator.parent
        while cls.is_dist_over(parent.__class__):
            operator, parent = parent, parent.parent
        return operator
    
    def both_operands_is_sum(self) -> bool:  return self.is_dist_over(self.one) and self.is_dist_over(self.two)
    @action('раскрыть скобку слева', both_operands_is_sum)
    def factor_in_left(self):
        print(f"factor_in_left: self.one = {self.one}")
        print(f"factor_in_left: self.two = {self.two}")
        sum_cls = self.one.__class__
        mul_cls = self.__class__
        nodes_list = self.one.to_list()
        for i, operand in enumerate(nodes_list): 
            nodes_list[i] = mul_cls(operand, deepcopy(self.two))
        new_sum = sum_cls.from_list(nodes_list)
        self.replace(new_sum)

    @action('раскрыть скобку справа', both_operands_is_sum)
    def factor_in_right(self) -> Node:
        sum_cls = self.two.__class__
        mul_cls = self.__class__
        nodes_list = self.two.to_list()
        for i, operand in enumerate(nodes_list): nodes_list[i] = mul_cls(deepcopy(self.one), operand)
        new_sum = sum_cls.from_list(nodes_list)
        self.replace(new_sum)

    def only_one_operand_is_sum(self) -> bool: return self.is_dist_over(self.one) != self.is_dist_over(self.two)
    @action('раскрыть скобку', only_one_operand_is_sum)
    def factor_in(self) -> Node:
        if self.is_dist_over(self.one): self.factor_in_left()
        if self.is_dist_over(self.two): self.factor_in_right()
       
class AssociativeCommutative(Associative, Commutative):
    @action('коммутативность')
    def commutative(self):
        self = self.associative()
        self.one, self.two = self.two, self.one 

    def __hash__(self):
        nodes_list = self.to_list()
        return hash((self.__class__,) + tuple(sorted(
            str(op.value) if isinstance(op, Value) else op.__class__.__name__
            for op in nodes_list)))
    
    def _equals(self, other) -> bool:
        self_flat = self.to_list() 
        other_flat = other.to_list()    
        return sorted(self_flat, key=hash) == sorted(other_flat, key=hash)

class AssociativeDistributive(Associative, Distributive):
    """
    @action('внести в скобку')
    @classmethod
    def factor_in(cls, node: Node, direction_right: bool = None):
        if direction_right is None:
            direction_right = cls.find_direction(node)
            if direction_right is None:
                return
        parent = node.parent
        is_left = node is parent.operands[0]
        if is_left == direction_right:
            super().factor_in(node)
        elif isinstance(parent.parent, cls):
            parent.parent.associative()
            super().factor_in(node)

    @classmethod
    def find_direction(cls, node: Node) -> bool | None:
        max_mult = cls.get_max_mult(node.parent)
        nodes_list = max_mult.to_list()
        node_index = nodes_list.index(node)
        left_is_sum = (node_index > 0 and nodes_list[node_index-1].__class__ in cls.distributive_over)
        right_is_sum = (node_index < len(nodes_list)-1 and nodes_list[node_index+1].__class__ in cls.distributive_over)
        return None if left_is_sum == right_is_sum else right_is_sum
    
    @classmethod
    def get_max_mult(cls, operator: Operator) -> Operator:
        parent = operator.parent
        while isinstance(parent, cls):
            operator, parent = parent, parent.parent
        return operator
    """
#####################################################################################

class Plus(AssociativeCommutative, Infix, Operator):         
    PRIORITY = 5

    def __init__(self, addend1, addend2): super().__init__(addend1, addend2)
          
    def __str__(self): return '+'

    def result(self) -> Node:
        if self.one == Number.ZERO: return self.two
        if self.two == Number.ZERO: return self.one
        try: return self.one + self.two
        except TypeError: return NotImplemented
          
class BinaryMinus(Infix, Operator):           
    PRIORITY = 5

    def __init__(self, minuend, subtrahend): super().__init__(minuend, subtrahend)

    def __str__(self): return '-'

    def result(self) -> Node:
        if self.one == Number.ZERO: return UnaryMinus(self.two)
        if self.two == Number.ZERO: return self.one
        try: return self.one - self.two
        except TypeError: return NotImplemented

    @action('представить как сумму')
    def as_plus(self):
        if isinstance(self.two, Number): self.replace(Plus(self.one, -self.two))  
        elif isinstance(self.two, UnaryMinus): self.replace(Plus(self.one, self.two.one))  
        else: self.replace(Plus(self.one, UnaryMinus(self.two)))
        
class Mult(AssociativeCommutative, AssociativeDistributive, Infix, Operator):
    distributive_over = (Plus, BinaryMinus)
                                   
    PRIORITY = 4    

    def __init__(self, factor1, factor2): super().__init__(factor1, factor2)
   
    def __str__(self): return '*'

    def result(self) -> Node:
        if self.one == Number.ONE: return self.two
        if self.two == Number.ONE: return self.one        
        if isinstance(self.one, Div) and isinstance(self.two,  Div): 
            return Div(Mult(self.one.one, self.two.one), Mult(self.one.two, self.two.two))
        try: return self.one * self.two
        except TypeError: return NotImplemented

class Div(Infix, Operator):           
    PRIORITY = 4

    def __init__(self, dividend, divisor): super().__init__(dividend, divisor)
 
    def __str__(self): return '/'

    def result(self) -> Node:
        if self.one == Number.ZERO: return Number(0)
        if self.two == Number.ONE: return self.one
        try: return self.one / self.two
        except TypeError: return NotImplemented
                   
class Pow(Infix, Operator):           
    PRIORITY = 2
    ASSOCIATIVITY_LEFT = False
    
    def __init__(self, base, degree): super().__init__(base, degree)
   
    def __str__(self): return '^'

    def result(self) -> Node:
        if self.two == Number.ONE: return self.one
        try: return self.one ** self.two
        except TypeError: return NotImplemented
        
class UnaryMinus(Prefix, Operator):
    ARITY = 1
    PRIORITY = 3       

    def __init__(self, operand): super().__init__(operand)
 
    def __str__(self): return '-'

    def result(self) -> Node:
        if isinstance(self.one, UnaryMinus): return self.one.one
        try: return -self.one
        except TypeError: return NotImplemented

class Sin(Prefix, Operator):
    ARITY = 1
    PRIORITY = 1                        

    def __int__(self, x): super().__init__(x)
    
    def __str__(self): return 'sin'

    def result(self) -> Node:
        try: return Number(math.sin(self.one))
        except TypeError: return NotImplemented
        
class Cos(Prefix, Operator):
    ARITY = 1
    PRIORITY = 1                         

    def __init__(self, x): super().__init__(x)
  
    def __str__(self): return 'cos'

    def result(self) -> Node:
        try: return Number(math.cos(self.one))
        except TypeError: return NotImplemented
        
class Log(Prefix, Operator):
    ARITY = 2                          
    PRIORITY = 1                         

    def __init__(self, base: Node, x: Node):
        if isinstance(base, Number):
            if base <= 0 or base == 1: raise ValueError(f'основание логарифма: {base}')
        super().__init__(base, x)

    def __str__(self): return 'log'

    def result(self) -> Node:
        try: return Number(math.log(self.two.value, self.one.value))
        except TypeError: return NotImplemented
        
class Lg(Prefix, Operator):
    ARITY = 1
    PRIORITY = 1                       

    def __init__(self, x: Node): super().__init__(x)

    def __str__(self): return 'lg'

    def result(self) -> Node:
        try: return Number(math.log(self.one.value, 10))
        except TypeError: return NotImplemented
    
class Ln(Prefix, Operator):
    ARITY = 1
    PRIORITY = 1                       

    def __init__(self, x: Node): super().__init__(x)
   
    def __str__(self): return 'ln'

    def result(self) -> Node:
        try: return Number(math.log(self.one.value, math.e))
        except TypeError: return NotImplemented
  
#####################################################################################        

def register_actions(cls=Node):
    for sub in cls.__subclasses__():
        sub.ACTIONS = {}
        for base in sub.__mro__: 
            for value in base.__dict__.values():
                if hasattr(value, 'action_name'):
                    sub.ACTIONS[value.action_name] = value
        register_actions(sub)

register_actions()
