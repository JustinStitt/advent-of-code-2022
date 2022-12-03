import sys
import string


total = 0
lineno = 0
elves = [None, None, None]
for line in sys.stdin.readlines():
    elves[lineno] = set(line.rstrip())
    lineno += 1
    if len(line) < 2:
        break
    do_inc = True
    if lineno == 3:
        print(elves)
        # calculate
        for (low, hi) in zip(string.ascii_lowercase, string.ascii_uppercase):
            if low in elves[0] and low in elves[1] and low in elves[2]:
                total += ord(low) - ord("a") + 1
                lineno = 0
                do_inc = False
                break
            elif hi in elves[0] and hi in elves[1] and hi in elves[2]:
                total += ord(hi) - ord("A") + 27
                lineno = 0
                do_inc = False
                break
        continue

print(total)
