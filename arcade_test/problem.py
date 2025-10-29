import parse
import nodes

class Problem():
    def __init__(self, root = nodes.Number(0)):
        self.root = root
        root.parent = self
        self.nodes_list = self.make_list()

    def make_list(self) -> list:
        def recursive_make_list(node: nodes.Node, parent=None, is_left=True) -> list:
            if isinstance(node, nodes.Value): 
                return [node]            
            if isinstance(node, nodes.Operator):
                if node.fixity is nodes.Fixity.PREFIX:
                    return [node, '('] + [o for op in node.operands for o in recursive_make_list(op, node)] + [')']                
                if node.fixity is nodes.Fixity.INFIX:
                    left, right = recursive_make_list(node.one, node, True), recursive_make_list(node.two, node, False)                    
                    for child, is_left_child, lst in [(node.one, True, left), (node.two, False, right)]:
                        if isinstance(child, nodes.Operator) and (
                            child.priority > node.priority or 
                            (child.priority == node.priority and 
                            ((node.associativity == nodes.Associativity.LEFT and not is_left_child) or
                            (node.associativity == nodes.Associativity.RIGHT and is_left_child)))
                        ):
                            lst[:] = ['('] + lst + [')']                    
                    return left + [node] + right                
                return ['('] + [o for op in node.operands for o in recursive_make_list(op, node)] + [')', node]
            return []
        return recursive_make_list(self.root)

    def __str__(self):
        string = ''
        for node in self.nodes_list:
            string += str(node) + ' '
        return string[:-1]
        
    def len_string(self): return len(str(self))
   
    def __getitem__(self, index): 
        return self.nodes_list[index]
    
    def __iter__(self): 
        return iter(self.nodes_list) 
    
    def __len__(self):
        return len(self.nodes_list)
    
    def get_node(self, index) -> nodes.Node:
        nodes_list = [node for node in self.nodes_list if isinstance(node, nodes.Node)]
        return nodes_list[index]
    
    def get_value(self, index) -> nodes.Value:
        values_list = [node for node in self.nodes_list if isinstance(node, nodes.Value)]
        return values_list[index]
    
    def get_operator(self, index) -> nodes.Operator:
        operators_list = [node for node in self.nodes_list if isinstance(node, nodes.Operator)]
        return operators_list[index]

    def operator_work(self, operator: nodes.Operator):
        operator.work()
        self.nodes_list = self.make_list()

    def operator_commutative(self, operator: nodes.Operator):
        operator.commutative()
        self.nodes_list = self.make_list()

####################################################################################

def create_problem(string) -> Problem: 
    root = parse.create_nodes_tree(string)
    return Problem(root)


A = create_problem('-(-(1, 2),+(3, 4))')
print(A)
A.operator_work(A.get_operator(1))
print(A)