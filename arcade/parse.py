import re
import nodes

operations : dict[str : type[nodes.Operator]] = {
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

operations_sorted = sorted(operations.keys(), key=len, reverse=True)
fist_chars_operations = {op[0] for op in operations.keys()}

def is_operator(token) -> bool:
    return token in operations

def is_number(string: str) -> bool:
    try: float(string); return True
    except ValueError: return False
    
def is_letter(string: str) -> bool:
    if not string[0].isalpha(): return False
    for char in string: 
        if not (char.isalnum()): return False
    if string in operations: return False
    return True

def remove_bracfast(string: str) -> str:
    while string.startswith('(') and string.endswith(')'):
        balance = 1
        for i in range(1, len(string) - 1):
            if string[i] == '(': balance += 1
            elif string[i] == ')':
                balance -= 1
                if balance == 0: return string 
        string = string[1:-1]
    return string

def find_last_operation(string: str):
    candidates = []
    balance = 0
    i = 0
    n = len(string)
    
    while i < n:
        char = string[i]
        if char == '(': balance += 1; i += 1; continue
        elif char == ')': balance -= 1; i += 1; continue        
        if char not in fist_chars_operations: i += 1; continue

        symbol = None; symbol_length = 0
        for op in operations_sorted:
            if string.startswith(op, i):
                if len(op) > 1:
                    if i > 0 and string[i-1].isalnum():
                        i += 1; continue
                    right_pos = i + len(op)
                    if right_pos < n and string[right_pos].isalnum() and string[right_pos] != '(':
                        i += 1; continue
                symbol = op
                symbol_length = len(op)
                break
            
        if symbol:
            if balance == 0:
                candidates.append((i, symbol, operations[symbol].PRIORITY))
            i += symbol_length 
        else: i += 1

    if not candidates: return None

    max_priority = max(c[2] for c in candidates)
    candidates = [(pos, sym) for pos, sym, pri in candidates if pri == max_priority]

    cls = operations[candidates[0][1]]

    if issubclass(cls, nodes.Infix) and not cls.ASSOCIATIVITY_LEFT: return candidates[0]
    else: return candidates[-1]
    
def infix_to_prefix(string: str) -> str:
    def recursive_infix_to_prefix(string: str) -> str: 
        string = remove_bracfast(string)
        if is_number(string) or is_letter(string): return string
        else:
            result = find_last_operation(string)
            if result is None: raise ValueError(f'не корректная строка {string}')
            
            position, symbol = result
            cls = operations[symbol]

            if issubclass(cls, nodes.Prefix):
                remaining = string[position + len(symbol):]
                
                balance = 1
                i = 1
                while i < len(remaining) and balance > 0:
                    if remaining[i] == '(': balance += 1
                    elif remaining[i] == ')': balance -= 1
                    i += 1
                
                inner = remaining[1:i-1]
                rest = remaining[i:] if i < len(remaining) else ''
                
                args = []
                current = ''
                balance = 0
                for char in inner:
                    if char == ',' and balance == 0:
                        args.append(current.strip())
                        current = ''
                    else:
                        current += char
                        if char == '(': balance += 1
                        elif char == ')': balance -= 1
                if current: args.append(current.strip())
                
                processed_args = [recursive_infix_to_prefix(arg) for arg in args]
                func_part = f'{symbol}({", ".join(processed_args)})'
                
                if rest: return recursive_infix_to_prefix(func_part + rest)
                return func_part

            elif issubclass(cls, nodes.Infix):
                left = recursive_infix_to_prefix(string[:position])
                right = recursive_infix_to_prefix(string[position + len(symbol):])
                return f'{symbol}({left},{right})'
            
    if not string: return None
    return recursive_infix_to_prefix(string.replace(' ', ''))

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

def infix_to_tree(string: str) -> nodes.Node: return prefix_to_tree(infix_to_prefix(string))