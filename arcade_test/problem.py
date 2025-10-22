import parse
import nodes

class Problem():
    def __init__(self, root = nodes.Number(0)):
        self.root = root
        root.parent = self
        self.nodes_list = self.make_list()

    def make_list(self) -> list:
        def recursive_make_list(node: nodes.Node) -> list:
            result = []
            if isinstance(node, nodes.Value): result = [node]
            elif isinstance(node, nodes.Operator):
                if node.fixity == nodes.Fixity.PREFIX:
                    result = [node, '(']
                    for o in node.operands:
                        result = result + recursive_make_list(o)
                    result = result + [')']
                elif node.fixity == nodes.Fixity.INFIX:
                    left = recursive_make_list(node.one)
                    right = recursive_make_list(node.two)
                    if isinstance(node.one, nodes.Operator):
                        if node.one.priority > node.priority: left = ['('] + left + [')']
                    if isinstance(node.two, nodes.Operator):
                        if node.two.priority > node.priority: right = ['('] + right + [')']
                    result = left + [node] + right  
                else:
                    result = ['(']
                    for o in node.operands:
                        result = result + recursive_make_list(o)
                    result = result + [')', node]
            return result
        return recursive_make_list(self.root)

    def __str__(self):
        string = ''
        for node in self.nodes_list:
            string += str(node)
        return string
        
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

    def operator_commutativity(self, operator: nodes.Operator):
        operator.commutative()
        self.nodes_list = self.make_list()

####################################################################################

def create_problem(string) -> Problem: 
    root = parse.create_nodes_tree(string)
    return Problem(root)


A = create_problem('+(a, +(1, +(2, 3)))')
print(A)
#print(A.root.print_tree())

A.operator_work(A.get_operator(1))

print(A)

A.operator_work(A.get_operator(0))

print(A)
#print(A.root.print_tree())