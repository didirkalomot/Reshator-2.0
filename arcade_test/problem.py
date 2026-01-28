import parse
import nodes

problem = parse.infix_to_tree('(1 + 34) * ~(sin(x) ^ 2 + cos(x) ^ 2)')

while True:
    problem.print_expression()
    index = input()
    if index == '': break
    elem = problem.nodes[int(index)]
    print(type(elem).__name__)
    action_name = input(f'{elem.actions}\n') 
    if action_name == '': break
    elem.do_action(action_name)











