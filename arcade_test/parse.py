import nodes

operations = {
    '^' : nodes.Pow,
    '~' : nodes.UnaryMinus,
    '*' : nodes.Mult,
    '/' : nodes.Div,
    '+' : nodes.Plus,
    '-' : nodes.BinaryMinus,
    'sin' : nodes.Sin,
    'cos' : nodes.Cos,
    'log' : nodes.Log, 
    'lg' : nodes.Lg,
    'ln' : nodes.Ln
}

def is_operator(token) -> bool:
    return token in operations

def is_number(string: str) -> bool:
    try: float(string); return True
    except ValueError: return False
    
def is_letter(string: str) -> bool:
    return len(string) > 0 and string[0].isalpha()

#def infix_to_prefix(string: str) -> str:
#    string = string.replace(' ', '')
#    for symbol in string:
#        if symbol in operations:
#            if isinstance(operations[symbol], nodes.Infix):


def prefix_to_tree(string: str) -> nodes.Node:
    string = string.replace(' ', '')
    stack = []
    i = 0
    tokens = []
    while i < len(string):
        if string[i] in '(),':
            tokens.append(string[i])
            i += 1
        else:
            start = i
            while i < len(string) and string[i] not in '(),':
                i += 1
            tokens.append(string[start:i])
    for token in tokens:
        if token == '(': stack.append('(')
        elif token == ')':
            args = []
            while stack and stack[-1] != '(': args.append(stack.pop())
            stack.pop()
            op_name = stack.pop()
            node = operations[op_name](*reversed(args))
            stack.append(node)
        elif token == ',': 
            continue
        else:
            if token in operations: stack.append(token)
            elif is_number(token): stack.append(nodes.Number(float(token)))
            elif is_letter(token): stack.append(nodes.Letter(token))
            else: raise ValueError(f'неизвестный токен: {token}')
    if len(stack) != 1: raise ValueError(f'недопустимое выражение')
    return stack[0]