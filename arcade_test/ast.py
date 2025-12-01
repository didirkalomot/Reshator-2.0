from copy import deepcopy
import enum
import math

def action(name):
    def decorator(func):
        func.action_name = name
        return func
    return decorator

class Node:
    actions = set()

    def __init_subclass__(cls):
        super().__init_subclass__()
        for attr_name in dir(cls):
            func = getattr(cls, attr_name) 
            if callable(func) and hasattr(func, 'action_name'): 
                cls.actions.add(func)
            
    __slots__ = ['parent']

    def __init__(self): self.parent = None

    def __str__(self): return 'node'

    def print_tree(self): print(f'[{self}]')

    def __deepcopy__(self, memo=None):
        cls = self.__class__
        result = cls.__new__(cls)
        result.parent = None
        return result

    def __eq__(self, other): return type(self) == type(other) and self._equals()
    
    def _equals(self, other) -> bool: raise NotImplementedError()
    
    def replace(self, new):
        if self.parent is not None:
            for i, oper in enumerate(self.parent.operands):
                if oper is self: 
                    self.parent.operands[i] = new
                    new.parent = self.parent

#####################################################################################

class Value(Node):
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value
        super().__init__()

    def __str__(self): return 'value'
    
    def __len__(self): return 1

    def _equals(self, other) -> bool: return self.value == other.value
    
    def __hash__(self): return hash((self.__class__, self.value))
    
    def __ne__(self, other): return not self == other

    def __deepcopy__(self, memo=None):
        result = super().__deepcopy__(memo)
        result.value = deepcopy(self.value, memo)
        return result
    
    @action('представить как противоположный')
    def as_neg(self): self.replace(UnaryMinus(UnaryMinus(self)))

    @action('представить как дробь')
    def as_fraction(self): self.replace(Div(self, Number(1)))

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

Number.zero = Number(0)
Number.one = Number(1)

class Letter(Value):
    def __init__(self, value: str):
        if value and value[0].isalpha():
            super().__init__(value)
        else: raise TypeError

    def __str__(self): return self.value

    def __len__(self): return len(self.value)

    def __add__(self, other):
        if self == other: return Mult(2, deepcopy(self))
        return NotImplemented
    
    def __sub__(self, other):
        if self == other: return Number(0)
        return NotImplemented
    
    def __mul__(self, other):
        if other == Number.zero: return Number(0)
        if self == other: return Pow(deepcopy(self), 2)
        return NotImplemented
    
    def __truediv__(self, other):
        if self == other: return Number(1)
        return NotImplemented

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

    __slots__ = ['operands']

    def __init__(self, *operands: Node):
        self.operands: list[Node] = list(operands)
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
        
    def _equals(self, other) -> bool:
        if len(self.operands) != len(other.operands): return False
        return all(a == b for a, b in zip(self.operands, other.operands))

    def __hash__(self):
        return hash((self.__class__,) + tuple(
            op.value if isinstance(op, Value) else op.__class__ 
            for op in self.operands
        ))
    
    def __deepcopy__(self, memo=None):
        result = super().__deepcopy__(memo)
        result.operands = deepcopy(self.operands, memo)
        for op in result.operands:
            op.parent = result
        return result
    
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

    def is_child(self, node: Node): 
        return any(operand is node for operand in self.operands)
    
    def is_descendant(self, node: Node):
        return (self is node or 
            any(isinstance(n, Operator) and n.is_descendant(node) 
                for n in self.operands))

    def result(self) -> Value: return NotImplemented

    @action('выполнить')
    def work(self):
        if (result := self.result()) != NotImplemented:
             self.replace(result)

    def solve(self):
        for i, operand in enumerate(self.operands):
            if isinstance(operand, Operator):
                new_operand = operand.solve()
                if new_operand is not operand:
                    self.operands[i] = new_operand
        result = self.work()
        return result if result != NotImplemented else self

#######################################

class Associative:
    @action('выполнить')
    def work(self):
        def do_work(operator):
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
        result = result.left_associative() \
        if result.associativity in (Associativity.BOTH, Associativity.LEFT) else result
        result = result.right_associative() \
        if result.associativity in (Associativity.BOTH, Associativity.RIGHT) else result
        return result
    
    @staticmethod
    def to_list(node) -> list[Node]:
        if node.associativity == Associativity.NONE:
            return node.operands
        operands = []
        def collect(n):
            if isinstance(n, node.__class__) and n.associativity != Associativity.NONE:
                for op in n.operands: collect(op)
            else: operands.append(n)
        collect(node)
        return operands
    
    @classmethod
    def from_list(cls, operands) -> Node | None:
        if not operands: return None
        if len(operands) == 1: return operands[0]
        if cls.associativity == Associativity.RIGHT:
            result = operands[-1]
            for i in range(len(operands)-2, -1, -1):
                result = cls(operands[i], result)
            return result
        else:
            result = operands[0]
            for op in operands[1:]: result = cls(result, op)
            return result

class Commutative:
    def __hash__(self):
        return hash((self.__class__,) + tuple(sorted(
            str(op.value) if isinstance(op, Value) else op.__class__.__name__
            for op in self.operands
        )))
    
    def _equals(self, other) -> bool:
        return sorted(self.operands, key=hash) == sorted(other.operands, key=hash)

    @action('коммутативность')
    def commutative(self):
        """a ∘ b → b ∘ a - поменять операнды местами"""
        if all(isinstance(oper, Value) for oper in self.operands):
            self.one, self.two = self.two, self.one

class Distributive:
    distributive_over: tuple[type[Associative], ...]

    @classmethod
    def factor_in(cls, node: Node):
        parent = node.parent
        left, right = parent.operands
        other = left if node is right else right
        sum_class = other.__class__
        if not cls.is_dist_over(sum_class): return

        create_node = (lambda operand: cls(deepcopy(node), operand)) \
        if node is left else (lambda operand: cls(operand, deepcopy(node)))
        
        nodes_list = sum_class.to_list(other)
        for i, operand in enumerate(nodes_list):
            nodes_list[i] = create_node(operand)
        new_sum = sum_class.from_list(nodes_list)
        parent.replace(new_sum)

    @classmethod
    def factor_out(cls, *args: Node):
        max_parent = cls.get_max_sum(args[0].parent)
        sum_class = max_parent.__class__
        if not cls.is_dist_over(sum_class):
            raise ValueError(f'{cls.__name__} не дистрибутивен над {sum_class.__name__}')
        if any(arg.parent.__class__ != cls for arg in args):
            raise ValueError('Разные операторы у аргументов')
        if any(arg != args[0] for arg in args[1:]):
            raise ValueError('Аргументы не равны')
        nodes_list = sum_class.to_list(max_parent)
        all_children = [child for op in nodes_list if isinstance(op, Operator) 
                       for child in op.operands]
        if any(arg not in all_children for arg in args):
            raise ValueError('Аргументы из разных сумм')
        
        touch_nodes = [
            op for op in nodes_list 
            if isinstance(op, Operator) and any(op.is_child(arg) 
            for arg in args)]
        other_nodes = [n for n in nodes_list if n not in touch_nodes]
        
        coefficients = []
        for arg in args:
            parent = arg.parent
            coefficients.append(
                parent.operands[1] 
                if parent.operands[0] == arg 
                else parent.operands[0])
            
        sum_of_coefs = sum_class.from_list(coefficients)
        factored_part = cls(sum_of_coefs, args[0])
        new_expression = (sum_class.from_list(other_nodes + [factored_part])
                         if other_nodes else factored_part)
        
        max_parent.replace(new_expression)

    @classmethod
    def get_max_sum(cls, operator: Operator) -> Operator:
        parent = operator.parent
        while cls.is_dist_over(parent.__class__):
            operator, parent = parent, parent.parent
        return operator
    
    @classmethod
    def is_dist_over(cls, node_cls: type) -> bool:
        return node_cls in cls.distributive_over
        
class AssociativeCommutative(Associative, Commutative):
    @action('коммутативность')
    def commutative(self):
        def do_commutative(operator):
            operator.one, operator.two = operator.two, operator.one
        do_commutative(self.associative())

    def __hash__(self):
        nodes_list = self.to_list(self)
        return hash((self.__class__,) + tuple(sorted(
            str(op.value) if isinstance(op, Value) else op.__class__.__name__
            for op in nodes_list
        )))
    
    def _equals(self, other) -> bool:
        self_flat = self.to_list(self) 
        other_flat = self.to_list(other)    
        return sorted(self_flat, key=hash) == sorted(other_flat, key=hash)

class AssociativeDistributive(Associative, Distributive):
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
        nodes_list = cls.to_list(max_mult)
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
    
#####################################################################################

class Plus(AssociativeCommutative, Operator):
    fixity = Fixity.INFIX 
    arity = 2             
    priority = 5
    associativity = Associativity.BOTH
    commutativity = True 

    def __init__(self, addend1, addend2): super().__init__(addend1, addend2)
        
    def __str__(self): return '+'

    def result(self) -> Node:
        if self.one == Number.zero: return self.two
        if self.two == Number.zero: return self.one
        try: return self.one + self.two
        except TypeError: return NotImplemented
          
class BinaryMinus(Associative, Operator):
    fixity = Fixity.INFIX 
    arity = 2            
    priority = 5
    associativity = Associativity.LEFT
    commutativity = False 

    def __init__(self, minuend, subtrahend): super().__init__(minuend, subtrahend)

    def __str__(self): return '-'

    def result(self) -> Node:
        if self.one == Number.zero: return UnaryMinus(self.two)
        if self.two == Number.zero: return self.one
        try: return self.one - self.two
        except TypeError: return NotImplemented

    @action('представить как сумму')
    def as_plus(self):
        if isinstance(self.two, UnaryMinus): 
            self.replace(Plus(self.one, self.two.one))  
        else:
            self.replace(Plus(self.one, UnaryMinus(self.two)))
        
class Mult(AssociativeCommutative, AssociativeDistributive, Operator):
    distributive_over = (Plus, BinaryMinus)

    fixity = Fixity.INFIX             
    arity = 2                          
    priority = 4
    associativity = Associativity.BOTH
    commutativity = True              

    def __init__(self, factor1, factor2): super().__init__(factor1, factor2)

    def __str__(self): return '*'

    def result(self) -> Node:
        if self.one == Number.one: return self.two
        if self.two == Number.one: return self.one        
        if isinstance(self.one, Div) and isinstance(self.two,  Div): 
            return Div(Mult(self.one.one, self.two.one), Mult(self.one.two, self.two.two))
        try: return self.one * self.two
        except TypeError: return NotImplemented

class Div(Associative, Operator):
    fixity = Fixity.INFIX 
    arity = 2             
    priority = 4
    associativity = Associativity.LEFT
    commutativity = False 

    def __init__(self, dividend, divisor): super().__init__(dividend, divisor)

    def __str__(self): return '/'

    def result(self) -> Node:
        if self.one == Number.zero: return Number(0)
        if self.two == Number.one: return self.one
        try: return self.one / self.two
        except TypeError: return NotImplemented
                   
class Pow(Associative, Operator):
    fixity = Fixity.INFIX 
    arity = 2             
    priority = 2
    associativity = Associativity.RIGHT
    commutativity = False
    
    def __init__(self, base, degree): super().__init__(base, degree)

    def __str__(self): return '^'

    def result(self) -> Node:
        if self.two == Number.one: return self.one
        try: return self.one ** self.two
        except TypeError: return NotImplemented
        
class UnaryMinus(Operator):
    fixity = Fixity.PREFIX
    arity = 1
    priority = 3
    associativity = Associativity.NONE 
    commutativity = False              

    def __init__(self, operand): super().__init__(operand)

    def __str__(self): return '-'

    def result(self) -> Node:
        if isinstance(self.one, UnaryMinus): return self.one.one
        try: return -self.one
        except TypeError: return NotImplemented

class Sin(Operator):
    fixity = Fixity.PREFIX
    arity = 1
    priority = 1   
    associativity = Associativity.NONE 
    commutativity = False                                   

    def __int__(self, x):
        super().__init__(x)

    def __str__(self): return 'sin'

    def result(self) -> Node:
        try: return Number(math.sin(self.one))
        except TypeError: return NotImplemented
        
class Cos(Operator):
    fixity = Fixity.PREFIX
    arity = 1
    priority = 1  
    associativity = Associativity.NONE 
    commutativity = False                                    

    def __init__(self, x):
        super().__int__(x)

    def __str__(self): return 'cos'

    def result(self) -> Node:
        try: return Number(math.cos(self.one))
        except TypeError: return NotImplemented
        
class Log(Operator):
    fixity = Fixity.PREFIX
    arity = 2                          
    priority = 1                       
    associativity = Associativity.NONE 
    commutativity = False              

    def __init__(self, base: Node, x: Node):
        if isinstance(base, Number):
            if base <= 0 or base == 1: raise ValueError(f'основание логарифма: {base}')
        super().__init__(base, x)

    def __str__(self): return 'log'

    def result(self) -> Node:
        try: return Number(math.log(self.two.value, self.one.value))
        except TypeError: return NotImplemented
        
class Lg(Operator):
    fixity = Fixity.PREFIX
    arity = 1
    priority = 1                       
    associativity = Associativity.NONE 
    commutativity = False 

    def __init__(self, x: Node):
        super().__init__(x)

    def __str__(self): return 'lg'

    def result(self) -> Node:
        try: return Number(math.log(self.one.value, 10))
        except TypeError: return NotImplemented
    
class Ln(Operator):
    fixity = Fixity.PREFIX
    arity = 1
    priority = 1                       
    associativity = Associativity.NONE 
    commutativity = False 

    def __init__(self, x: Node):
        super().__init__(x)

    def __str__(self): return 'ln'

    def result(self) -> Node:
        try: return Number(math.log(self.one.value, math.e))
        except TypeError: return NotImplemented
  
#####################################################################################        