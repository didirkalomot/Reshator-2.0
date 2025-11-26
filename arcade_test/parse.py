import ast

operations = {
    '^' : ast.Pow,
    '~' : ast.UnaryMinus,
    '*' : ast.Mult,
    '/' : ast.Div,
    '+' : ast.Plus,
    '-' : ast.BinaryMinus,
    'sin' : ast.Sin,
    'cos' : ast.Cos,
    'log' : ast.Log, 
    'lg' : ast.Lg,
    'ln' : ast.Ln
}

def create_ast_tree(string: str) -> ast.Node:

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

    def recursive_create_ast(string: str) -> ast.Node:
        if is_number(string): return ast.Number(float(string)); 
        elif is_letter(string): return ast.Letter(string)    
        else:
            end_name = string.find('(')
            name = string[:end_name]
            if not is_operation(name): raise ValueError(f'не корректная строка: "{string}"')

            operands = find_all_operands(string[end_name+1:-1])

            node_operands = []
            for operand in operands:
                if operand:
                    node = recursive_create_ast(operand)
                    node_operands.append(node)

            return operations[name](*node_operands)
        
        
    string = string.replace(' ', '')
    return recursive_create_ast(string)   