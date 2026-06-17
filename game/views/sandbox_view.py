from __future__ import annotations
from mechanics import parse
from game.views.expression_view import ExpressionView

######################################## Режим Со Случайным Примером ########################################

class SandboxMode(ExpressionView):
    def __init__(self):
        root = parse.random_expression()
        # Если по какой-то причине вернулся None – подставим заглушку
        if root is None:
            root = nodes.Number(1)
        super().__init__(root)
