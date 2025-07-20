class Node:
    def __init__(self, left = None, right = None):
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

#####################################################################################

class Node:
    def __init__(self, left=None, right=None):
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
    def __init__(self, value: float):
        super().__init__(value)
        if value.is_integer():
            self.value = int(value)
        else:
            self.value = value

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
        super().__init__(value)

    def __str__(self):
        return self.value

class Operator(Node):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)

    def __str__(self):
        return 'operator'

    def work(self):
        raise NotImplementedError("This method should be implemented by subclasses")

class Plus(Operator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __str__(self):
        return '+'

    def work(self):
        return self.left + self.right

class Minus(Operator):
    def __init__(self, left, right=None):
        if right is None:
            right = left
            left = None
        super().__init__(left, right)

    def __str__(self):
        return '-'

    def work(self):
        if self.left is None:
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

#####################################################################################

class Problem():
    def __init__(self, node: Node = Node()):
        self.root = node

    @staticmethod
    def recursive_str(node: Node):
        if node is not None:
            return Problem.recursive_str(node.left) + ' ' + str(node) + ' ' + Problem.recursive_str(node.right)
        else:
            return ''

    def __str__(self):
        return Problem.recursive_str(self.root).strip()
    
    def find_parent(self, current: Node, child: Node):
        if current is None:
            return None
        if current.left == child or current.right == child:
            return current
        left_result = self.find_parent(current.left, child)
        if left_result is not None:
            return left_result
        return self.find_parent(current.right, child)

    def use_operator(self, operator: Operator):
        if not isinstance(operator, Operator): 
            return 
            
        result = operator.work()
        
        if operator == self.root:
            self.root = result 
        else:
            parent = self.find_parent(self.root, operator)
            if parent is not None:
                if parent.left == operator:
                    parent.left = result
                elif parent.right == operator:
                    parent.right = result   
                                   
a = Number(3)
b = Number(4)
c = Number(5)

mult = Mult(b, c)
minus =  Minus(a)
plus = Plus(minus, mult)
problem = Problem(plus)

print(problem)

problem.use_operator(mult)

print(problem)
