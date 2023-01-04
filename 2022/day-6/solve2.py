import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]


for line in lines:
    for (i, c) in enumerate(line[: len(line) - 13]):
        chunk = set(line[i : i + 14])
        if chunk and len(chunk) == 14:
            print(chunk)
            print(i + 14)
            break
