######################################## Типы Токенов ########################################

class Token: 
    def __len__(self): return 0

class VisibleToken(Token):
    def __len__(self): return len(str(self))

class Bracket: # Миксин
    def __init__(self): self.pair: Bracket

######################################## Скобки ########################################

class NestedBeginToken(Bracket, Token):
    def __init__(self):
        super().__init__()
        self.operator: Token
    def __str__(self): return '['

class NestedEndToken(Bracket, Token):
    def __str__(self): return ']'

class OrderBracketLeftToken(Bracket, VisibleToken):
    def __str__(self): return '('

class OrderBracketRightToken(Bracket, VisibleToken):
    def __str__(self): return ')'

class FunctionBracketLeftToken(Bracket, VisibleToken):
    def __str__(self): return '('

class FunctionBracketRightToken(Bracket, VisibleToken):
    def __str__(self): return ')'

####################################### Фабрика Скобок #######################################

class BracketFactory:
    def __init__(self, left_cls, right_cls):
        self.left_cls = left_cls
        self.right_cls = right_cls
    
    def create_pair(self):
        left = self.left_cls()
        right = self.right_cls()
        left.pair = right
        right.pair = left
        return left, right
    
brackets = BracketFactory(OrderBracketLeftToken, OrderBracketRightToken)
function_brackets = BracketFactory(FunctionBracketLeftToken, FunctionBracketRightToken)

####################################### Фабрика Токенов Вложения #######################################

class NestedFactory(BracketFactory):
    def __init__(self, left_cls, right_cls):
        super().__init__(left_cls, right_cls)

    def create_pair(self, operator):
        left, right = super().create_pair()
        left.operator = operator
        return left, right

nested_bounds = NestedFactory(NestedBeginToken, NestedEndToken)
