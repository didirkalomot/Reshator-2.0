class Node:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def __str__(self): return 'node'
    
    def __len__(self): return 0

    def recursive_len(self) -> int:
        if self.left != None: left_size = self.left.recursive_len() + 1
        else: left_size = 0
        if self.right != None: right_size = self.right.recursive_len() + 1
        else: right_size = 0
        return left_size + len(self) + right_size
    
class Value(Node):
    def __init__(self, value):
        super().__init__()
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
        if len(value) == 1 and value.isalpha():
            super().__init__(value)
        else: raise TypeError

    def __str__(self): return self.value

    def __len__(self): return len(self.value)

class Operator(Node):
    def __init__(self, priority, left=None, right=None):
        super().__init__(left, right)
        self.priority = priority

    def __str__(self): return 'operator'
    
    def __len__(self): return 1 

    def recursive_len(self) -> int:
        result = super().recursive_len()
        if isinstance(self.left, Operator):
            if self.left.priority < self.priority: result += 2
        if isinstance(self.right, Operator):
            if self.right.priority < self.priority: result += 2
        return result

    def work(self):pass

class Minus(Operator):
    def __init__(self, left, right=None):
        if right is None:
            right = left
            left = None
            super().__init__(1, left, right)
            return
        super().__init__(2, left, right)

    def __str__(self):
        return '-'

    def work(self):
        try:
            if self.left is None:
                return -self.right
            else:
                return self.left - self.right
        except:
            return None
        
class Plus(Operator):
    def __init__(self, left, right):
        super().__init__(2, left, right)

    def __str__(self):
        return '+'

    def work(self):
        try:
            return self.left + self.right
        except:
            return None
        
class Pow(Operator):
    def __init__(self, left, right):
        super().__init__(3, left, right)

    def __str__(self):
        return '^'

    def work(self):
        try:
            return self.left ** self.right
        except:
            return None
        
class Mult(Operator):
    def __init__(self, left, right):
        super().__init__(4, left, right)

    def __str__(self):
        return '*'

    def work(self):
        try:
            return self.left * self.right
        except:
            return None

class Div(Operator):
    def __init__(self, left, right):
        super().__init__(4, left, right)

    def __str__(self):
        return '/'

    def work(self):
        try:
            return self.left / self.right
        except:
            return None
        
#####################################################################################

class Bad(Exception):
    def __init__(self, current : Node, damage):
        self.current = current
        self.damage = damage
    
class PriorityError(Bad):
    def __init__(self, current : Node):
        super().__init__(current, 1)

    def __str__(self):
        return 'не тот порядок действий'

#####################################################################################

class Problem():
    def __init__(self, node: Node = Number(0)):
        self.root = node

    def __str__(self):
        def recursive_str(node: Node) -> str:
            if node is not None:
                left_string = recursive_str(node.left)
                right_string =  recursive_str(node.right)
                if isinstance(node, Operator):
                    if isinstance(node.left, Operator):
                        if node.left.priority < node.priority:
                            left_string = '(' + left_string[1:-1] + ')'
                    if isinstance(node.right, Operator):
                        if node.right.priority < node.priority:
                            right_string = '(' + right_string[1:-1] + ')'
                return left_string + ' ' + str(node) + ' ' + right_string
            else:
                return ''
        return recursive_str(self.root)
    
    def __len__(self):
        return len(str(self))
    
    def print_tree(self):
        def recursive_print_tree(node: Node, depth = 0):
            if node is None: return
            string = '-' * depth + '[' + str(node) + ']'
            print(string)
            recursive_print_tree(node.left, depth+1)
            recursive_print_tree(node.right, depth+1)
        recursive_print_tree(self.root)

    def find_parent(self, current: Node, child: Node):
        if current is None:
            return None
        if current.left == child or current.right == child:
            return current
        left_result = self.find_parent(current.left, child)
        if left_result is not None:
            return left_result
        return self.find_parent(current.right, child)

    def use_operator(self, operator: Operator) -> Value:
        if not isinstance(operator, Operator): 
            return None
        result = operator.work()
        if result is None: raise PriorityError(operator)
        if operator == self.root:
            self.root = result 
        else:
            parent = self.find_parent(self.root, operator)
            if parent is not None:
                if parent.left == operator:
                    parent.left = result
                elif parent.right == operator:
                    parent.right = result   
        return result

#####################################################################################

symbols_operators = {
    '+' : Plus,
    '-' : Minus,
    '*' : Mult,
    '/' : Div,
    '^' : Pow
}

def make_problem(string: str) -> Problem:
    string = string.replace(' ', '')

    def get_priority(char: str) -> int:
        if char not in symbols_operators: return None
        return symbols_operators[char](None, None).priority
    
    def remove_brackets(string):
        if len(string) < 2 or string[0] != '(' or string[-1] != ')':
            return string
        depth = 1
        for ch in string[1:-1]:
            if ch == '(': depth += 1; continue
            if ch == ')': depth -= 1; continue
            if depth == 0:
                return string
        return string[1:-1]

    def find_root_index(string):
        depth = 0
        index = None
        last_priority = None

        for i, ch in enumerate(string):
            if ch == '(': depth += 1; continue
            if ch == ')': depth -= 1; continue
            if depth != 0: continue
            
            priority = get_priority(ch)
            if i == 0 and ch == '-': priority = 1
            if priority != None:
                if last_priority == None: last_priority = priority
                if priority >= last_priority:
                    last_priority = priority
                    index = i
        if index == None: print(string)
        return index
    
    def make_value(string: str) -> Value:
        try:
            return Number(float(string))
        except: 
            try:
                return Letter(string)
            except: 
                return None

    def recursive_make_node(string: str) -> Node:
        string = remove_brackets(string)
        if string == '' or string == ' ' or string == None: return None

        value = make_value(string)
        if value != None: return value

        index = find_root_index(string)
        char = string[index]
        left = string[:index]
        right = string[index+1:]
        node = symbols_operators[char](recursive_make_node(left), recursive_make_node(right))
        return node
            
    root = recursive_make_node(string)
    return Problem(root)

#####################################################################################