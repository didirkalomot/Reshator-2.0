from __future__ import annotations
from mechanics import parse
from game.views.base import ExpressionMode

######################################## Режим Со Случайным Примером ########################################

class QuadraticEquationMode(ExpressionMode): 
    def __init__(self): 
        string = 'a^2 + -25*a + 100 = 80'
        super().__init__(parse.create_tree(string))
