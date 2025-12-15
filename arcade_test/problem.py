import parse
import ast

class Problem():
    def update_list(self):
        def needs_parentheses(parent, child, is_left) -> bool:
            if not isinstance(child, ast.Operator): return False
            if child.priority > parent.priority: return True
            if child.__class__ != parent.__class__:
                if isinstance(parent, ast.Plus) and isinstance(child, ast.BinaryMinus) \
                or isinstance(parent, ast.BinaryMinus) and isinstance(child, ast.Plus): return False 
                return True
            if parent.associativity is ast.Associativity.LEFT and not is_left: return True  
            if parent.associativity is ast.Associativity.RIGHT and is_left: return True     
            return False
        def recursive_make_list(node: ast.Node, parent=None, is_left: bool=None) -> list:
            if isinstance(node, ast.Value): return [node]
            if isinstance(node, ast.Operator):
                if node.fixity is ast.Fixity.PREFIX:
                    return [node, '('] + [o for operand in node.operands for o in recursive_make_list(operand, node)] + [')']
                if node.fixity is ast.Fixity.INFIX:
                    left, right = recursive_make_list(node.one, node, True), recursive_make_list(node.two, node, False)
                    for child, is_left, lst in [(node.one, True, left), (node.two, False, right)]:
                        if needs_parentheses(node, child, is_left): lst[:] = ['('] + lst + [')']
                    return left + [node] + right
                return ['('] + [o for operand in node.operands for o in recursive_make_list(operand, node)] + [')', node]
            return []
        self.problem_list = recursive_make_list(self.root)
                            
    def __init__(self, root = ast.Number(0)):
        self.operands = [root]
        root.parent = self
        self.update_list()

    @property
    def root(self): return self.operands[0]
    
    @root.setter
    def root(self, new):
        self.operands[0] = new
        new.parent = self
        self.update_list()

    def replace_root(self, new_node): self.operands[0] = new_node

    def print_tree(self): self.operands[0].print_tree()

    def __str__(self):
        string = ''
        for node in self.problem_list:
            string += str(node) + ' '
        return string[:-1]
        
    def len_string(self): return len(str(self))
   
    def __getitem__(self, index): 
        return self.problem_list[index]
    
    def __iter__(self): 
        return iter(self.problem_list) 
    
    def __len__(self):
        return len(self.problem_list)
    
    @property
    def nodes(self) -> list[ast.Node]:
        return [node for node in self.problem_list if isinstance(node, ast.Node)]
    
    @property
    def values(self) -> list[ast.Value]:
        return [value for value in self.problem_list if isinstance(value, ast.Value)]
    
    @property
    def operators(self) -> list[ast.Operator]:
        return [operator for operator in self.problem_list if isinstance(operator, ast.Operator)]  
    
    def use_action(self, node: ast.Node, action_name):
        if node in self.problem_list: 
            node.actions[action_name]()
            self.update_list()

    def work(self, operator: ast.Operator):
        if operator in self.problem_list:
            operator.work()
            self.update_list()

    def commutative(self, operator: ast.Operator):
        if operator in self.problem_list and isinstance(operator, ast.Commutative):
            operator.commutative()
            self.update_list()

    def factor_out(self, *args: ast.Node):
        if args[0] in self.problem_list:
            distributive_class = args[0].parent.__class__
            if issubclass(distributive_class, ast.Distributive):
                distributive_class.factor_out(*args)
                self.update_list()

    def factor_in(self, node: ast.Node, direction_right: bool = None):
        if node in self.problem_list:
            distributive_class = node.parent.__class__
            if issubclass(distributive_class, ast.Distributive):
                distributive_class.factor_in(node, direction_right)
                self.update_list()

####################################################################################

def create_problem(string) -> Problem:
    root = parse.create_ast_tree(string)
    return Problem(root)

####################################################################################

#A = create_problem('*(a, +(b, -(c, d)))')

Root = parse.create_ast_tree('*(a, +(b, -(c, d)))')

for node in Root.two:
    print(node)

