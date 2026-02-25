import parse
import nodes

root = parse.infix_to_tree('(a + b) * (2 + 4)')

while True:
    root.print_expression()
    index = input()
    if index == '': break
    elem = root.nodes[int(index)]
    print(elem.__class__.__name__)
    action_name = input(f'{elem.actions}\n') 
    if action_name == '': break
    elem.do_action(action_name)












