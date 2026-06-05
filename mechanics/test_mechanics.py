import nodes
import parse
import exceptions

root = parse.create_tree('- 3 + 4 + 5 - 3 - 5')
for t in root:
    print(str(t), end=' ')
print('ff')

root.print_tree()

