import sys

a = sum(
    [
        1
        if (a >= c and a <= d)
        or (b >= c and b <= d)
        or (c >= a and c <= b)
        or (d >= a and d <= b)
        else 0
        for (a, b, c, d) in [
            (*i.split("-"), *ii.split("-"))
            for (i, ii) in [l.split(",") for l in sys.stdin.readlines()]
        ]
    ]
)

print(a)
# 2-4 3-5
# 16-30 19-24
