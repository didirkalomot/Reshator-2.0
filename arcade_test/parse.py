import nodes

operations = {
    '^' : nodes.Pow,
    '~' : nodes.UnaryMinus,
    '*' : nodes.Mult,
    '/' : nodes.Div,
    '+' : nodes.Plus,
    '-' : nodes.BinaryMinus,
    #'sin' : nodes.Sin,
    #'cos' : nodes.Cos,
    #'log' : nodes.Log, 
}

def create_problem_tree(string: str) -> nodes.Node:

    def is_operation(string: str) -> bool:
        return string in operations
    
    def is_number(string: str) -> bool:
        string = string.replace('.', '')
        return string.isdigit() or (string[0] == '-' and string[1:].isdigit())
    
    def is_letter(string: str) -> bool:
        return string[0].isalpha and (len(string) == 1 or string[1:].isdigit())
    
    def find_all_operands(string: str) -> list[str]:
        balance = 0
        operands = []
        start = 0
        
        for i, char in enumerate(string):
            if char == '(': balance += 1; continue
            if char == ')': balance -= 1; continue
            if balance == 0 and char == ',':
                operands.append(string[start:i])
                start = i + 1
        
        operands.append(string[start:])
        return operands

    def recursive_create_nodes(string: str) -> nodes.Node:
        if is_number(string): return nodes.Number(float(string))
        elif is_letter(string): return nodes.Letter(string)
        else:
            end_name = string.find('(')
            name = string[:end_name]
            if not is_operation(name): raise ValueError(f'не корректная строка: "{string}"')

            operands = find_all_operands(string[end_name+1:-1])

            node_operands = []
            for operand in operands:
                if operand:  # проверяем, что операнд не пустой
                    node = recursive_create_nodes(operand)
                    node_operands.append(node)

            return operations[name](*node_operands)
        
    string = string.replace(' ', '')
    return recursive_create_nodes(string)

        
        