import sys
from dataclasses import dataclass

lines = [line.rstrip() for line in sys.stdin.readlines()]
indices = {}
order = []
nums = []

key = 811589153
# key = 1


@dataclass
class Num:
    num: int = 0


for (idx, line) in enumerate(lines):
    num = Num(int(line) * key)
    indices[int(line)] = idx
    order.append(num)  # stores pointers to order
    nums.append(num)


def rotate(idx, offset):
    global nums, order
    if offset == 0:
        return
    bigger = offset > len(nums)
    if offset < 0:
        offset = abs(offset) % (len(nums) - 1)
        offset = len(nums) - offset - 1

    for _ in range((abs(offset) % (len(nums) - 1))):
        nidx = (idx + 1) % len(nums)
        nums[idx], nums[nidx] = nums[nidx], nums[idx]
        idx = nidx


# print("initial: ")
# for n in nums:
#     print(n.num, end=", ")
# print()
# print()
for mixno in range(10):
    print(f"{mixno=}")
    idx = 0
    while idx < len(order):
        to_find = order[idx]
        for (i, num) in enumerate(nums):
            if to_find is num:
                # print(f"moving {i=}, {num=}")
                rotate(i, num.num)
                break
        idx += 1
    # for n in nums:
    #     print(n.num, end=", ")
    # print()
    # break

zero_idx = 9999
# find the idx of zero
for (i, num) in enumerate(nums):
    if num.num == 0:
        zero_idx = i
total = 0
for m in range(3):
    nidx = zero_idx + 1000 * (m + 1)
    nidx %= len(nums)
    print(nums[nidx].num)
    total += nums[nidx].num

print("Total: ", total)
