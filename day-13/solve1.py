import sys
import functools

lines = [line.rstrip() for line in sys.stdin.readlines()]
# idea... make everything a list even single ints
pairs = []
correct = 0


def solve(first, last):
    # print(f"{first=}, {last=}")
    # print(type(first), "\t", type(last))
    if type(first) is int and type(last) is int:
        if first < last:
            return 1
        if first > last:
            return 0
        if first == last:
            return 2
    if type(first) is int and type(last) is list:
        first = [first]
    elif type(last) is int and type(first) is list:
        last = [last]
    res = 1
    if type(first) is list and type(last) is list:
        i = 0
        while 1:
            if i > len(first) - 1 and len(last) > len(first):
                return 1
            if i > len(last) - 1 and len(first) > len(last):
                return 0
            if i > len(last) - 1 and i > len(first) - 1:
                return 2
            x, y = first[i], last[i]
            # print(f"{x=}, {y=}")
            hres = solve(x, y)
            # print(f"{hres=}")
            if hres == 0:
                return 0
            if hres == 1:
                return 1
            i += 1

        # for (x, y) in zip(first, last):
    return 2


i = 0
for idx in range(0, len(lines) - 1, 3):
    i += 1
    p1, p2 = lines[idx], lines[idx + 1]
    p1 = eval(p1)
    p2 = eval(p2)
    # print(p1, p2)
    # check pair
    ans = 1
    ans = solve(p1, p2)

    # print(f"\n{ans=}")
    if ans == 1:
        pairs.append(i)

    # print(first, " ", last)

# print(pairs)
# print(sum(pairs))


many = list(filter(lambda x: len(x), lines))
many = [eval(x) for x in many]
# add markers
m1 = [[2]]
m2 = [[6]]
many.append(m1)
many.append(m2)
# many = sorted(many, key=functools.cmp_to_key(solve))

# selection sort
for x in range(len(many) - 1):
    for y in range(x + 1, len(many)):
        rezzi = solve(many[x], many[y])
        if rezzi == 0:  # x is less than y
            # no swap needed
            pass
        elif rezzi == 1:  # x is greater than y ... swap needed
            many[x], many[y] = many[y], many[x]
        elif rezzi == 2:  # don't move
            pass
        # print(rezzi)
many = many[::-1]
i1 = many.index(m1) + 1
i2 = many.index(m2) + 1
print(i1, i2)
print(i1 * i2)
