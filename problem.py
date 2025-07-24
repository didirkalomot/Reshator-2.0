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
    def __init__(self, priority = 1, left=None, right=None):
        super().__init__(left, right)
        self.priority = priority

    def __str__(self):
        return 'operator'

    def work(self):pass

class Plus(Operator):
    def __init__(self, left, right):
        super().__init__(1, left, right)

    def __str__(self):
        return '+'

    def work(self):
        try:
            return self.left + self.right
        except:
            return None

class Minus(Operator):
    def __init__(self, left, right=None):
        if right is None:
            right = left
            left = None
            super().__init__(9, left, right)
            return
        super().__init__(1, left, right)

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
        
class Mult(Operator):
    def __init__(self, left, right):
        super().__init__(2, left, right)

    def __str__(self):
        return '*'

    def work(self):
        try:
            return self.left * self.right
        except:
            return None

class Div(Operator):
    def __init__(self, left, right):
        super().__init__(2, left, right)

    def __str__(self):
        return '/'

    def work(self):
        try:
            return self.left / self.right
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
        
#####################################################################################

class Bad(Exception):
    def __init__(self, current : Node, damage):
        self.current = current
        self.damage = damage
    
class NotOperatorDefinition(Bad):
    def __init__(self, current : Node):
        super().__init__(current, 3)

    def __str__(self):
        return f'нет оператора "{str(self.current)}" для классов: {type(self.current.left).__name__} и {type(self.current.right).__name__}'

#####################################################################################

class Problem():
    def __init__(self, node: Node = Node()):
        self.root = node

    def __str__(self):
        def recursive_str(node: Node):
            if node is not None:
                return recursive_str(node.left) + ' ' + str(node) + ' ' + recursive_str(node.right)
            else:
                return ''
        return recursive_str(self.root)
    
    def print_tree(self):
        def recursive_print_tree(node: Node, depth = 0):
            if node is None: return
            string = '-' * depth + type(node).__name__+ ' ' + str(node)
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

    def use_operator(self, operator: Operator):
        if not isinstance(operator, Operator): 
            return     
        result = operator.work()
        if result is None: raise NotOperatorDefinition(operator)
        if operator == self.root:
            self.root = result 
        else:
            parent = self.find_parent(self.root, operator)
            if parent is not None:
                if parent.left == operator:
                    parent.left = result
                elif parent.right == operator:
                    parent.right = result   

#####################################################################################

symbols_operators_dict = {
    '+' : Plus,
    '-' : Minus,
    '*' : Mult,
    '/' : Div,
    '^' : Pow
}

def make_problem(string: str) -> Problem:
    def problem_string_to_list(string: str):
        nodes_list = string.split(' ')
        for i, ch in enumerate(nodes_list):
            try: 
                number = float(ch)
                nodes_list[i] = Number(number)
            except:
                if ch in symbols_operators_dict:
                    nodes_list[i] = symbols_operators_dict[ch](None, None)
                elif ch.isalpha() and len(ch) == 1: nodes_list[i] = Letter(ch)
                else: raise TypeError   
        return nodes_list

    def find_root(nodes: list) -> Node:
        last_operator = None
        for node in nodes:
            if isinstance(node, Operator): last_operator = node
        for node in nodes:
            if isinstance(node, Operator):
                if node.priority <= last_operator.priority:
                    last_operator = node
        return last_operator

    def recursive_make_problem(nodes: list) -> Node:
        if nodes is None or len(nodes) == 0: return
        if len(nodes) == 1: return nodes[0]
        root = find_root(nodes)
        left = nodes[:nodes.index(root)]
        right = nodes[nodes.index(root)+1:]
        root.left = recursive_make_problem(left)
        root.right = recursive_make_problem(right)
        return root
    
    nodes = problem_string_to_list(string)
    root = recursive_make_problem(nodes)
    return Problem(root)

#####################################################################################

problem = make_problem('- 33 / 5 + -4 * 3')
print(problem)

problem.use_operator(problem.root.right)
print(problem)

problem.use_operator(problem.root.left.left)
print(problem)

problem.use_operator(problem.root.left)
print(problem)

problem.use_operator(problem.root)
print(problem)

#problem.print_tree()

