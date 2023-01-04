import sys, functools
import subprocess

lines = [line.rstrip() for line in sys.stdin.readlines()]


class Monkey:
    def __init__(self):
        self.starting = []
        self.operation = lambda x: x + 777
        self.divi = lambda x: True
        self.throw_to = {True: -1, False: -1}
        self.inspect_count = 0

    def calculate(self, x: int):
        # op = self.operation.replace("old", str(x))
        # result = subprocess.run(
        #     ["echo " f"$(({op}))", " | ", "bc"], shell=True, stdout=subprocess.PIPE
        # )
        if "*" in self.operation:
            rhs = self.operation[self.operation.index("*") + 2 :]
            if "o" in rhs:
                rhs = x
            rhs = int(rhs)
            return x * rhs
        else:
            rhs = self.operation[self.operation.index("+") + 2]
            rhs = int(rhs)
            return x + rhs
        # return int(result.stdout.decode("utf-8"))

    def test(self, x):

        passes = x % self.divi == 0
        return self.throw_to[passes]


BIG_DIVISOR = 1
# monkeys = [None] * 256
monkeys = []
for idx in range(0, len(lines), 7):
    grouping = lines[idx : idx + 6]
    midx, strt, op, tst, t, f = grouping
    midx = int(midx[midx.index(":") - 1])
    to_add = Monkey()
    strt = strt[strt.index(":") + 1 :].split(",")
    strt = [int(x) for x in strt]
    to_add.starting = strt
    # op
    op = op[op.index("=") + 2 :]
    to_add.operation = op
    tst = tst[tst.index("y") + 2 :]
    to_add.divi = int(tst)
    print(f"{to_add.divi=}")
    t = t[t.index("y") + 2 :]
    f = f[f.index("y") + 2 :]
    to_add.throw_to = {True: int(t), False: int(f)}
    monkeys.append(to_add)
    monkeys[midx] = to_add

print("START")
for monkey in monkeys:
    print(monkey.starting)
    BIG_DIVISOR *= monkey.divi
# print(monkeys)
num_rounds = 10_000
for round in range(num_rounds):
    if round % 100 == 0:
        print("Round: ", round)
    for currm in monkeys:
        for item in currm.starting:
            new_worry_level = currm.calculate(item)
            new_worry_level = new_worry_level % BIG_DIVISOR
            # print(
            #     f"Worry before {item} ... Worry after {new_worry_level} ... operation: {currm.operation}"
            # )
            currm.inspect_count += 1
            # new_worry_level = new_worry_level // 3 # pt 2 removed this!
            go_to = currm.test(new_worry_level)
            monkeys[go_to].starting.append(
                new_worry_level
            )  # throw item to proper monkey (delegate)
        currm.starting = []
    # print("Round: ", round)
    # for monkey in monkeys:
    #     print(monkey.starting)

best_two = sorted(monkeys, key=lambda m: m.inspect_count)[-2:]
print(best_two[0].inspect_count * best_two[1].inspect_count)
# test_monkey = Monkey()
# test_monkey.operation = "old * 19"
# print(test_monkey.calculate(5))
