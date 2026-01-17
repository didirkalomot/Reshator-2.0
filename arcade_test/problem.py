import parse
import nodes

Root = parse.prefix_to_tree('*(*(1, 2), *(3, *(4, 5)))')

print(Root)
Root.operators[0].work()
print(Root)



