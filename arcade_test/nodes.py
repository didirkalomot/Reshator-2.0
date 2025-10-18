import copy

class Value:
    def __init__(self, value):
        self.parent = None
        self.value = value

    def __str__(self): return 'value'
    
    def __len__(self): return 1

class Number(Value):
    def __init__(self, value: float):
        super().__init__(value)
        if value.is_integer():
            self.value = int(value)
        else:
            self.value = value

    def __str__(self): return str(self.value)
    
    def __len__(self): return len(str(self.value))

    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
        return None

    def __neg__(self):
        return Number(-self.value)

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

class Node:
    def __init__(self, *childs):
        self.parent = None
        self.operands = list(childs)
        for node in self.operands:
            node.parent = self

    def __str__(self): return 'node'

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
    
    def __len__(self): return 0

    def __copy__(self):
        return copy.deepcopy(self)
    
    def replace(self, new):
        if self.parent is not None:
            for i, oper in enumerate(self.parent.operands):
                if oper is self:
                    self.parent.operands[i] = new
                    new.parent = self.parent
                    return

class Operator(Node):
    priority=None

    def __init__(self, *operands: Node):
        super().__init__(*operands)

    @property
    def arity(self):
        return len(self.operands)

    def __str__(self): return 'operator'
    
    def __len__(self): return 1 

    def result(self) -> Value: return None

    def work(self):
        if all(isinstance(oper, Value) for oper in self.operands):
            result = self.result()
            if result is not None:
                if self.parent is not None:
                    self.replace(result)
            return result
        return None

    def solve(self):
        for i, operand in enumerate(self.operands):
            if isinstance(operand, Operator):
                new_operand = operand.solve()
                if new_operand is not operand:
                    self.operands[i] = new_operand
        result = self.work()
        return result if result is not None else self
        
#######################################

class Unary:
    @property
    def one(self):
        return self.operands[0]

class Binary(Unary): 
    @property
    def two(self):
        return self.operands[1]

class Ternary(Binary):
    @property
    def three(self):
        return self.operands[2]
    
#######################################

class Pow(Operator, Binary):
    priority=2
    
    def __init__(self, one, two):
        super().__init__(one, two)

    def __str__(self):
        return '^'

    def result(self) -> Value:
        try:
            return self.one ** self.two
        except:
            return None

class UnaryMinus(Operator, Unary):
    priority=3

    def __init__(self, one):
        super().__init__(one)

    def __str__(self): return '-'

    def result(self) -> Value:
        try:
            return -self.one
        except:
            return None
               
class Mult(Operator, Binary):
    priority=4

    def __init__(self, one, two):
        super().__init__(one, two)

    def __str__(self):
        return '*'

    def result(self) -> Value:
        try:
            return self.one * self.two
        except:
            return None

class Div(Operator, Binary):
    priority=4

    def __init__(self, one, two):
        super().__init__(one, two)

    def __str__(self):
        return '/'

    def result(self) -> Value:
        try:
            return self.one / self.two
        except:
            return None
        
class BinaryMinus(Operator, Binary):
    priority=5

    def __init__(self, one, two):
        super().__init__(one, two)

    def __str__(self): return '-'

    def result(self):
        try:
            return self.one - self.two
        except: 
            return None
                
class Plus(Operator, Binary):
    priority = 5

    def __init__(self, one, two):
        super().__init__(one, two)
        
    def __str__(self):
        return '+'

    def result(self) -> Value:
        try:
            return self.one + self.two
        except:
            return None
        
#####################################################################################        