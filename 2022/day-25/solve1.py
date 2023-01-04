import sys
from dataclasses import dataclass

lines = [line.rstrip() for line in sys.stdin.readlines()]

snafus = []
for line in lines:
    snafus.append(line)


def snafuToDec(snafu):
    ans = 0
    for i in range(len(snafu)):
        padded = snafu[i] + "0" * (len(snafu) - i - 1)
        padded = padded.replace("-", "-1")
        padded = padded.replace("=", "-2")
        to_add = int(padded, base=5)
        ans += to_add
        # print(padded, to_add)
    return ans


class Node:
    def __init__(self, data, left=None):
        self.data = data
        self.left = left

def decToSnafu(dec):
    # try right to left strat (seems weird)
    base5 = numberToBase(dec, 5)
    prev = Node(base5[0])
    nodes = []
    for i in range(1, len(base5)):
        to_add = Node(base5[i], prev)
        nodes.append(to_add)
        prev = to_add

    curr = prev
    right_most = prev
    carry = 0
    # print(f"{base5=}")
    # now walk the list, adding new nodes if oob
    while curr is not None:
        # print(f"{curr.data=}")
        curr.data += carry
        carry = 0
        if curr.data == 5:
            curr.data = 0
            carry = 1
        if curr.data in (0, 1, 2):
            # if going left is None but we have a carry, make a new node!
            if curr.left is None and carry > 0:
                new_node = Node(carry)
                curr.left = new_node
                curr = new_node
            curr = curr.left
            continue
        if curr.data in (3, 4):
            curr.data = "=" if curr.data == 3 else "-"
            carry = 1
            if curr.left is None and carry > 0:
                new_node = Node(carry)
                curr.left = new_node
                curr = new_node
            curr = curr.left

    # print(base5)
    print("printing list")
    out = []
    while right_most is not None:
        out.append(right_most.data)
        right_most = right_most.left
    return out[::-1]


def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


print(snafus)
total = 0
for snafu in snafus:
    rezzi = snafuToDec(snafu)
    rezzi2 = numberToBase(rezzi, 5)
    if "=" in snafu or "-" in snafu:
        print(f"{rezzi=}, {snafu=}, {rezzi2=}, ")
    total += rezzi
    # print(f"{snafu=}, dec={snafuToDec(snafu)}")

print(total)
result = decToSnafu(total)
for c in result:
    print(c, end="")
print()
# print(snafuToDec("12="))
# res = decToSnafu(total)
# for c in res:
#     print(c, end="")
# print()

# decToSnafuTwo(2022)
# decToSnafuTwo(12345)
# decToSnafuTwo(314159265)
