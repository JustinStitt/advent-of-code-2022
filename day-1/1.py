import sys

groups = []
lines = []
curr = 0
for line in sys.stdin:
    line = line.strip()
    if line != "":
        curr += int(line)
    lines.append(line.strip())
    if line == "":
        groups.append(curr)
        curr = 0

groups = sorted(groups)
# print(groups[-1])
# print(groups[-2])
# print(groups[-3])

print(sum(groups[-3:]))
