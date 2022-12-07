import sys
from collections import defaultdict

lines = [line.rstrip() for line in sys.stdin.readlines()]

ls = "$ ls"
cd = "$ cd"
dirsizes = defaultdict(lambda: int())
dirsizes_dep = defaultdict(lambda: set())
deep = {}
dirstack = []

reading_ls_mode = False
for line in lines:
    if "$" in line:
        reading_ls_mode = False
    if reading_ls_mode:
        deep[dirstack[-1]] = len(dirstack)
        if "dir" in line:
            _adir = line[4:]
            # add this to dirsizes dependency
            dirsizes_dep[dirstack[-1]].add(_adir)
            dirsizes[dirstack[-1]] += 0
        else:
            # read file size
            fsize = line[: line.index(" ")]
            dirsizes[dirstack[-1]] += int(fsize)
    if ls in line:
        # read to next command
        reading_ls_mode = True
        continue
    if cd in line:
        adir = line[5:]
        if ".." in line:
            dirstack.pop()
        else:
            dirstack.append(adir)

# print(dirsizes)
# print(dirsizes_dep)
new_sizes = defaultdict(lambda: int())
total = 0

sorted_deep = sorted(list(deep.items()), key=lambda x: x[1], reverse=True)
# print(sorted_deep)
for (directory, depth) in sorted_deep:
    actual = dirsizes[directory]
    for inner in dirsizes_dep[directory]:
        actual += dirsizes[inner]
    dirsizes[directory] = actual

for (directory, sz) in dirsizes.items():
    if sz <= 100_000:
        print(directory, " ", sz, deep[directory])
        total += sz

print("test: ", dirsizes["gwlwp"])
# print(sorted_deep)
print(total)
# 1062847
# 1037318
