import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]


for line in lines:
    for (i, c) in enumerate(line[: len(line) - 3]):
        chunk = set(line[i : i + 4])
        if chunk and len(chunk) == 4:
            print(chunk)
            print(i + 4)
            break
