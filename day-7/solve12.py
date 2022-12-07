import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]

ls = "$ ls"
cd = "$ cd"

total_space = 70_000_000
need = 30_000_000


class Directory:
    def __init__(self, me="", parent=None, du=0, children=dict()):
        self.me = me
        self.parent = parent
        self.du = du
        self.children = children


ls_mode = False
root = Directory(me="/")
curr = root

for line in lines[1:]:
    if "$" in line:
        ls_mode = False
    if ls_mode:
        if "dir" in line:
            to_add = Directory(me=line[4:], parent=curr, children=dict())
            curr.children[line[4:]] = to_add
        else:
            curr.du += int(line[: line.index(" ")])

    if cd in line:
        if ".." in line:
            # print("up:", curr.children)
            curr = curr.parent
        else:
            # print(curr.children)
            curr = curr.children[line[5:]]

    if ls in line:
        ls_mode = True

# visited = set()

total = 0

opts = []


all = []


def dfs(node):
    global total
    for (_dir, child) in node.children.items():
        node.du += dfs(child)
    # if node.du <= 100_000:
    # total += node.du
    all.append(node.du)
    return node.du


dfs(root)

unused = total_space - root.du
amnt = need - unused
print(unused)
print(amnt)
for diskusage in all:
    if diskusage >= amnt:
        opts.append(diskusage)
print(opts)
# print(root.du)

print(total)
print(sorted(opts)[0])
