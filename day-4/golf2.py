import sys

a = sum(
    1 if (len(n) + len(m)) > len(set(n) | set(m)) else 0
    for (n, m) in [
        (range(int(a), int(b) + 1), range(int(c), int(d) + 1))
        for (a, b, c, d) in [
            (*i.split("-"), *ii.split("-"))
            for (i, ii) in [l.split(",") for l in sys.stdin.readlines()]
        ]
    ]
)

print(a)
# 2-4 3-5
# 16-30 19-24
