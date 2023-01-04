import sys

score = 0
for line in sys.stdin.readlines():
    (o, m) = line.rstrip().split()
    delta = (ord(o) - ord("A")) - (ord(m) - ord("X"))
    score += ord(m) - ord("X") + 1
    if abs(delta) == 2:
        score += 0 if delta < 0 else 6
        continue
    score += 3 if not delta else 0 if delta == 1 else 6
print(score)
