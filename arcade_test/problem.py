import parse
import nodes

Root = parse.prefix_to_tree('*(+(a, b), 2)')

while True:
    index = input(f'{Root}\n')
    if index == '': break
    elem = Root.nodes[int(index)]
    print(type(elem).__name__)
    action_name = input(f'{elem.actions}\n') 
    if action_name == '': break
    elem.do_action(action_name)




