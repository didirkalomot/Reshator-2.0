######################################## Типы Токенов ########################################

class Token: 
    def __len__(self): return 0

class VisibleToken(Token):
    def __len__(self): return len(str(self))

class Bracket:
    def __init__(self): self.pair: Bracket

######################################## Скобки ########################################

class LayoutBeginToken(Token, Bracket):
    def __str__(self): return '['

class LayoutEndToken(Token, Bracket):
    def __str__(self): return ']'

class OrderBracketLeftToken(VisibleToken, Bracket):
    def __str__(self): return '('

class OrderBracketRightToken(VisibleToken, Bracket):
    def __str__(self): return ')'

class FunctionBracketLeftToken(VisibleToken, Bracket):
    def __str__(self): return '('

class FunctionBracketRightToken(VisibleToken, Bracket):
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

layout_bounds = BracketFactory(LayoutBeginToken, LayoutEndToken)
brackets = BracketFactory(OrderBracketLeftToken, OrderBracketRightToken)
function_brackets = BracketFactory(FunctionBracketLeftToken, FunctionBracketRightToken)