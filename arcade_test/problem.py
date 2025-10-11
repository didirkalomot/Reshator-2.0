class Good(Exception):pass

class Bad(Exception):
    def __init__(self, current, damage):
        self.current = current
        self.damage = damage

class UnknownVariable(Bad):
    def __int__(self, current):
        super().__init__(current, 1)

    def __str__(self):
        return 'один из операндов - неизвестная переменная'
    
class WrongPriority(Bad):
    def __init__(self, current):
        super().__init__(current, 1)

    def __str__(self):
        return 'не тот порядок действий'
class NoCommutativity(Bad):
    def __init__(self, current):
        super().__init__(current, 2)

    def __str__(self):
        return 'нет коммутативности'

#####################################################################################

class Node:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def __str__(self): return 'node'
    
    def __len__(self): return 0

    """
    def recursive_len(self) -> int:
        if self.left != None: left_size = self.left.recursive_len() + 1
        else: left_size = 0
        if self.right != None: right_size = self.right.recursive_len() + 1
        else: right_size = 0
        return left_size + len(self) + right_size
    """

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
    def __init__(self, left=None, right=None, priority = 1, commutativity = False, associativity = False):
        super().__init__(left, right)
        self.priority = priority
        self.commutativity = commutativity
        self.associativity = associativity

    def __str__(self): return 'operator'
    
    def __len__(self): return 1 

    """
    def recursive_len(self) -> int:
        result = super().recursive_len()
        if isinstance(self.left, Operator):
            if self.left.priority < self.priority: result += 2
        if isinstance(self.right, Operator):
            if self.right.priority < self.priority: result += 2
        return result
    """

    def work(self):
        if isinstance(self.left, Operator): raise WrongPriority(self.left)
        if isinstance(self.left, Letter): raise UnknownVariable(self.left)

        if isinstance(self.right, Operator): raise WrongPriority(self.rigth)
        if isinstance(self.right, Letter): raise UnknownVariable(self.right)


class Minus(Operator):
    def __init__(self, left, right=None):
        if right is None:
            right = left
            left = None
            super().__init__(left, right, 2)
            return
        super().__init__(left, right, 4)

    def __str__(self):
        return '-'

    def work(self):
        super().work()
        try:
            if self.left is None:
                return -self.right
            else:
                return self.left - self.right
        except:
            return None
        
class Plus(Operator):
    def __init__(self, left, right):
        super().__init__(left, right, 4, True, True)

    def __str__(self):
        return '+'

    def work(self):
        super().work()
        try:
            return self.left + self.right
        except:
            return None
        
class Pow(Operator):
    def __init__(self, left, right):
        super().__init__(left, right, 1)

    def __str__(self):
        return '^'

    def work(self):
        super().work()
        try:
            return self.left ** self.right
        except:
            return None
        
class Mult(Operator):
    def __init__(self, left, right):
        super().__init__(left, right, 3, True, True)

    def __str__(self):
        return '*'

    def work(self):
        super().work()
        try:
            return self.left * self.right
        except:
            return None

class Div(Operator):
    def __init__(self, left, right):
        super().__init__(left, right, 3)

    def __str__(self):
        return '/'

    def work(self):
        super().work()
        try:
            return self.left / self.right
        except:
            return None
        
#####################################################################################


class ProblemTree():
    def __init__(self, node: Node = Number(0)):
        self.root = node

    def __str__(self):
        def recursive_str(node: Node) -> str:
            if node is not None:
                left_string = recursive_str(node.left)
                right_string =  recursive_str(node.right)
                if isinstance(node, Operator):
                    if isinstance(node.left, Operator):
                        if node.left.priority > node.priority:
                            left_string = '(' + left_string[1:-1] + ')'
                    if isinstance(node.right, Operator):
                        if node.right.priority > node.priority:
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

    def use_operator(self, operator: Operator):
        if not isinstance(operator, Operator): return 
        result = operator.work()
        if result is None: return
        if operator == self.root:
            self.root = result 
        else:
            parent = self.find_parent(self.root, operator)
            if parent is not None:
                if parent.left == operator:
                    parent.left = result
                elif parent.right == operator:
                    parent.right = result   
    
    def use_commutativity(self, operator: Operator):
        if not isinstance(operator, Operator): return
        if not operator.commutativity: raise NoCommutativity(operator)

        operator.left, operator.right = operator.right, operator.left

#####################################################################################

symbols_operators = {
    '+' : Plus,
    '-' : Minus,
    '*' : Mult,
    '/' : Div,
    '^' : Pow
}

def make_problem_tree(string: str) -> ProblemTree:
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
    return ProblemTree(root)

#####################################################################################

class ProblemList(ProblemTree):
    def __init__(self, node: Node = Number(0)):
        super().__init__(node)
        self.nodes_list = self.make_list()

    def make_list(self) -> list:
        def recursive_make_list(node : Node) -> list:
            if node is None: return []
            if isinstance(node, Value):
                return [node]
            elif isinstance(node, Operator):
                left = recursive_make_list(node.left)
                right = recursive_make_list(node.right)
                if isinstance(node.left, Operator):
                    if node.left.priority > node.priority: left = ['('] + left + [')']
                if isinstance(node.right, Operator):
                    if node.right.priority > node.priority:  right = ['('] + right + [')'] 
                return left + [node] + right
        
        return recursive_make_list(self.root)

    def __str__(self):
        string = ''
        nodes_iter = iter(self.nodes_list)
        for node in nodes_iter:
            string += str(node) 
            if node != '(': string += ' '
            if node == ')':
                string += '\b\b\b) '
        return string
    
    def len_string(self):
        return len(str(self))
   
    def __getitem__(self, index): 
        return self.nodes_list[index]
    
    def __iter__(self): 
        return iter(self.nodes_list) 
    
    def len_list(self):
        return len(self.nodes_list)
    
    def get_node(self, index) -> Node:
        nodes_list = [node for node in self.nodes_list if isinstance(node, Node)]
        return nodes_list[index]
    
    def get_value(self, index) -> Value:
        values_list = [node for node in self.nodes_list if isinstance(node, Value)]
        return values_list[index]
    
    def get_operator(self, index) -> Operator:
        operators_list = [node for node in self.nodes_list if isinstance(node, Operator)]
        return operators_list[index]

    def use_operator(self, operator):
        super().use_operator(operator)
        self.nodes_list = self.make_list()

    def use_commutativity(self, operator):
        super().use_commutativity(operator)
        self.nodes_list = self.make_list()

#####################################################################################

def make_problem_list(string: str) -> ProblemList:
    tree = make_problem_tree(string)
    return ProblemList(tree.root)

#####################################################################################