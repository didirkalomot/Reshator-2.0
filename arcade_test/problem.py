import parse
import nodes


root = parse.create_problem_tree('+(1,2)')

#####################################################################################

class Problem():
    def __init__(self, node = Number(0)):
        self.root = node
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

    def operator_work(self, operator):
        operator.work()
        self.nodes_list = self.make_list()

    def operator_commutativity(self, operator):
        super().operator_commutativity(operator)
        self.nodes_list = self.make_list()

####################################################################################


