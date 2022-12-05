import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]


delim = "X"
stacks = [0] * 16
last_at = 0
for (i, line) in enumerate(lines):
    if line == delim:
        pass
    if "1" in line:
        last_at = i
        break
    for (i, c) in enumerate(line):
        if c == " ":
            continue
        idx = i // 4
        if stacks[idx] and c != " ":
            stacks[idx].append(c)
            continue

        stacks[idx] = [c]

# now read move froms
for line in lines[last_at + 2 :]:
    ls = line.split()
    amnt, fro, to = ls[1], ls[3], ls[5]
    amnt = int(amnt)
    fro = int(fro) - 1
    to = int(to) - 1
    # make the move
    for ii in range(amnt):
        top_of_fro = stacks[fro].pop(amnt - 1 - ii)
        stacks[to].insert(0, top_of_fro)

# top of each stack
for stack in stacks:
    if stack == 0:
        continue
    print(stack.pop(0), end="")
