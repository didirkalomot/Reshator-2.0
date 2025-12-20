import parse

Root = parse.create_nodes_tree('/(+(5, *(+(a, b), 10)), 5)')

print(Root)
print(Root.operators[2].actions)



