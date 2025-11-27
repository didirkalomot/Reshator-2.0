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

def is_operator(token) -> bool:
    return token in operations

def is_number(string: str) -> bool:
    try: float(string); return True
    except ValueError: return False
    
def is_letter(string: str) -> bool:
    return len(string) > 0 and string[0].isalpha()

"""
def infix_to_prefix(expression: str) -> str:
    def build_prefix_string(tokens):
        stack = []
        for token in reversed(tokens):
            if token in operations:
                op_class = operations[token]
                arity = op_class.arity if op_class.arity is not None else 2
                operands = []
                for _ in range(arity):
                    if not stack:
                        raise ValueError(f"Not enough operands for {token}")
                    operands.append(stack.pop())
                stack.append(f"{token}({','.join(operands)})")
            else:
                stack.append(token)
        if len(stack) != 1:
            raise ValueError("Invalid expression structure")
        return stack[0]
    
    precedence = {}
    fixity_info = {}
    
    for symbol, op_class in operations.items():
        precedence[symbol] = op_class.priority
        fixity_info[symbol] = op_class.fixity
    
    def get_operator_fixity(op_symbol):
        return fixity_info[op_symbol]
    
    operator_chars = set()
    for symbol in operations.keys():
        operator_chars.update(symbol)
    
    separator_chars = {'(', ')', ',', ' '}
    all_special_chars = operator_chars | separator_chars
    
    tokens = []
    i = 0
    expr = expression.replace(' ', '')
    
    while i < len(expr):
        if expr[i] == '-' and (i == 0 or expr[i-1] in '(,' or expr[i-1] in operator_chars):
            tokens.append('~') 
            i += 1
        elif expr[i] in all_special_chars:
            found_multi_char = False
            for op in sorted(operations.keys(), key=len, reverse=True):
                if expr.startswith(op, i) and (len(op) > 1 or expr[i] in operator_chars):
                    tokens.append(op)
                    i += len(op)
                    found_multi_char = True
                    break
            
            if not found_multi_char:
                if expr[i] in operator_chars | {'(', ')', ','}:
                    tokens.append(expr[i])
                    i += 1
                else:
                    raise ValueError(f"Unexpected character: {expr[i]}")
        else:
            start = i
            while i < len(expr) and expr[i] not in all_special_chars:
                i += 1
            token = expr[start:i]
            tokens.append(token)
    
    output = []
    stack = []
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if token == '~':
            stack.append('~')
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError('не сбалансированны скобки')
            stack.pop()
        elif is_operator(token):
            fixity = get_operator_fixity(token)
            
            if fixity == ast.Fixity.INFIX:
                while (stack and stack[-1] != '(' and 
                       precedence.get(stack[-1], 0) >= precedence.get(token, 0)):
                    output.append(stack.pop())
                stack.append(token)
            elif fixity == ast.Fixity.PREFIX:
                stack.append(token)
        else:
            output.append(token)
        i += 1

    while stack:
        if stack[-1] == '(':
            raise ValueError("Unbalanced parentheses")
        output.append(stack.pop())
    
    return build_prefix_string(output)
"""

def create_ast_tree(string: str) -> ast.Node:
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
            elif is_number(token): stack.append(ast.Number(float(token)))
            elif is_letter(token): stack.append(ast.Letter(token))
            else: raise ValueError(f'неизвестный токен: {token}')
    if len(stack) != 1: raise ValueError(f'недопустимое выражение')
    return stack[0]