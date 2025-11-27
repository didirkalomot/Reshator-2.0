import parse
import ast

class Problem():
    def update_list(self) -> list:
        def recursive_make_list(node: ast.Node, parent=None, is_left=True) -> list:
            if isinstance(node, ast.Value): 
                return [node]            
            if isinstance(node, ast.Operator):
                if node.fixity is ast.Fixity.PREFIX:
                    return [node, '('] + [o for operand in node.operands for o in recursive_make_list(operand, node)] + [')']                
                if node.fixity is ast.Fixity.INFIX:
                    left, right = recursive_make_list(node.one, node, True), recursive_make_list(node.two, node, False)                    
                    for child, is_left_child, lst in [(node.one, True, left), (node.two, False, right)]:
                        if isinstance(child, ast.Operator) and (
                            child.priority > node.priority or 
                            (child.priority == node.priority and 
                            ((node.associativity == ast.Associativity.LEFT and not is_left_child) or
                            (node.associativity == ast.Associativity.RIGHT and is_left_child)))
                        ):
                            lst[:] = ['('] + lst + [')']                    
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

    def work(self, operator: ast.Operator):
        operator.work()
        self.update_list()

    def commutative(self, operator: ast.Operator):
        if isinstance(operator, ast.Commutative):
            operator.commutative()
            self.update_list()

    def factor_out(self, *args: ast.Node):
        distributive_class = args[0].parent.__class__
        if issubclass(distributive_class, ast.Distributive):
            distributive_class.factor_out(*args)
            self.update_list()

    def factor_in(self, node: ast.Node, direction_right: bool = None):
        distributive_class = node.parent.__class__
        if issubclass(distributive_class, ast.Distributive):
            distributive_class.factor_in(node, direction_right)
            self.update_list()

####################################################################################

def create_problem(string) -> Problem: 
    root = parse.create_ast_tree(string)
    return Problem(root)

A = create_problem('*(*(+(+(1, 2), +(3, 4)), a), b)')
print(A)