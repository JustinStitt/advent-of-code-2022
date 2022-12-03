import sys
from collections import defaultdict


total = 0
for line in sys.stdin.readlines():
    rucksack = line.rstrip()
    comp1 = rucksack[: len(rucksack) // 2]
    comp2 = rucksack[len(rucksack) // 2 :]
    uset = set(comp1)

    for item in comp2:
        if item in comp1:
            if item >= "a" and item <= "z":
                total += ord(item) - ord("a") + 1
                break
            else:
                total += ord(item) - ord("A") + 27
                break
        else:
            uset.add(item)

print("total:", total)
