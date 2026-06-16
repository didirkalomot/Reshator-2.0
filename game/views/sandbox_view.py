from __future__ import annotations
from mechanics import parse
from game.views.expression_view import ExpressionView

######################################## Режим Со Случайным Примером ########################################

class SandboxMode(ExpressionView): 
    def __init__(self): super().__init__(parse.random_expression())