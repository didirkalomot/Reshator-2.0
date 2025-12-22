import parse

Root = parse.create_nodes_tree('/(+(5, *(+(3, 2), 10)), 5)')

print(Root)
print(Root.operators[0].actions)
