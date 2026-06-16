from __future__ import annotations
from mechanics import parse
from game.views.expression_view import ExpressionView

######################################## Режим Со Случайным Примером ########################################

class QuadraticEquationMode(ExpressionView): 
    def __init__(self): 
        string = 'a^2 - a + 10 = 0'
        super().__init__(parse.create_tree(string))
