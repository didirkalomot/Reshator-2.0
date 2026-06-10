import nodes
import parse
import exceptions

root1 = parse.create_tree('4 + 2')
root2 = parse.create_tree('6')

print(root1 == root2)


