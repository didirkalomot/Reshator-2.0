import parse
import ast

Root = parse.create_ast_tree('*(a, +(b, -(c, d)))')

for node in Root.two:
    print(node)

