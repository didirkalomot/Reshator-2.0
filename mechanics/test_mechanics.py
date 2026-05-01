import nodes
import parse
import exceptions

root = parse.infix_to_tree('1 + 2 * 3')
root.print_expression()
root.print_tree()


