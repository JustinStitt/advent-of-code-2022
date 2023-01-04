import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]

instructions = []
X = 1
cycle = 0
mod = 20
logs = []
for line in lines:
    cycle += 1  # start of cycle
    logs.append(X)
    if "noop" in line:
        # consume cycle
        continue
    op, num = line.split()
    # is addx
    # run both cycles of current instruction
    logs.append(X)
    X += int(num)
    cycle += 1

care = [20, 60, 100, 140, 180, 220]

total = 0
for c in care:
    total += logs[c - 1] * c
    print(logs[c - 1])

print(total)
