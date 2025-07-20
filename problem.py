class Node:
    def __init__(self, left= None, right = None):
        self.left = left
        self.right = right

    def __str__(self):
        return 'node'

class Value(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return 'value'

class Number(Value):
    def __init__(self, value : float):
        super().__init__(value)
        if value.is_integer(): self.value = int(value)
        else: self.value = value

    def __str__(self):
        return str(self.value)  
    
    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
        return None
        
    def __neg__(self):
        return Number(-self.value)
    
    def __sub__(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.other)
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
    def __init__(self, value : str):
        super().__init__(value)

    def __str__(self):
        return self.value
    
class Operator(Node):
    def __init__(self, left = None, right = None):
        super().__init__(left, right)

    def __str__(self):
        return 'operator'

    def work(self):
        print('work')

class Plus(Operator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __str__(self):
        return '+'
    
    def work(self):
        return self.left + self.right
    
class Minus(Operator):
    def __init__(self, left, right = None):
        if right == None: right, left = left, None
        super().__init__(left, right)

    def __str__(self):
        return '-'
    
    def work(self):
        if self.left == None:
            return -self.right 
        else: 
            return self.left - self.right
    
class Mult(Operator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __str__(self):
        return '*'
    
    def work(self):
        return self.left * self.right

class Div(Operator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __str__(self):
        return '/'
    
    def work(self):
        return self.left / self.right
    
class Pow(Operator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __str__(self):
        return '^'
    
    def work(self):
        return self.left ** self.right

######################################################################################################################################

class Problem():
    def __init__(self, node : Node = Node()):
        self.root = node

    def recursive_str(node : Node):
        if node != None:
            return Problem.recursive_str(node.left) + ' ' + node.__str__() + ' ' + Problem.recursive_str(node.right)
        else: return ''

    def __str__(self):
        return Problem.recursive_str(self.root)
    
    def use_operator(self, operator : Operator):
        if not isinstance(operator, Operator): return 
        if operator.work() != None: operator = operator.work()
                                   
a = Number(3)
b = Number(4)
c = Number(5)

mult = Mult(b, c)
minus =  Minus(a)
plus = Plus(minus, mult)
problem = Problem(plus)

print(problem)

