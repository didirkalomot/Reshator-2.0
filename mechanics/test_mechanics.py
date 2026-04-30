import nodes
import parse
import exceptions

root = parse.infix_to_tree('1 + 2 + 3 = a * b')
root.print_expression()


