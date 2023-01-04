import sys
from aocdebug.debug import debug

DEBUG = False
debug = debug if DEBUG else lambda _: 0

lines = [line.rstrip() for line in sys.stdin.readlines()]

count = 0
vowels = "aeiou"
cant = ["ab", "cd", "pq", "xy"]


for line in lines:
    vowel_count = sum(1 if c in vowels else 0 for c in line)
    if vowel_count < 3:
        continue
    has_double = any(line[i] == line[i + 1] for i in range(len(line) - 1))
    if not has_double:
        continue

    has_bad = any(bad in line for bad in cant)
    if has_bad:
        continue
    debug(line)
    count += 1

print(f"Total: {count}")
