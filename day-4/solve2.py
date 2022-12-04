import sys
import math

lines = sys.stdin.readlines()  # 2-4,4-6

total = 0
for line in lines:
    lhs, rhs = line.split(",")
    # construct lhs range
    idx = lhs.index("-")
    idxr = rhs.index("-")
    lhs_range = range(int(lhs[0:idx]), int(lhs[idx + 1 :]) + 1)
    rhs_range = range(int(rhs[0:idxr]), int(rhs[idxr + 1 :]) + 1)
    for n in lhs_range:
        if n in rhs_range:
            total += 1
            break
print(total)
