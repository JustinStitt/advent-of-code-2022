import sys
from collections import defaultdict

lines = [line.rstrip() for line in sys.stdin.readlines()]


class Monkey:
    def __init__(self, name, number, is_expr, lhs=None, rhs=None, op=None):
        self.name = name
        self.number = number
        self.is_expr = is_expr
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def __repr__(self):
        return f"Monkey({self.name=}, {self.number=}, {self.is_expr=}, {self.lhs=}, {self.op=}, {self.rhs=})"

    def solve(self):
        global monkeys
        # print(f"Solving for: {self.name}")
        if self.is_expr is False:
            return self.number  # nothing to solve, just ret number

        # solve each of lhs or rhs
        lhs_result = (monkeys[self.lhs]).solve()
        rhs_result = (monkeys[self.rhs]).solve()
        self.number = eval(f"{lhs_result} {self.op} {rhs_result}")
        self.is_expr = False
        self.lhs = None
        self.rhs = None
        self.op = None
        return self.number


monkeys = {}
for line in lines:
    sp = line.split()
    name = line[: line.index(":")]
    if len(sp) == 2:  # just a number, monkey
        num = int(line[line.index(" ") + 1 :])
        nm = Monkey(name, num, is_expr=False)
        monkeys[name] = nm
    else:  # it's a expr, get both pieces and op
        lhs, op, rhs = sp[1:]
        nm = Monkey(name, None, is_expr=True, lhs=lhs, rhs=rhs, op=op)
        # exprs[name] = f"{lhs} {op} {rhs}"
        monkeys[name] = nm

root = monkeys["root"]
# root.op = "="  # pt 2 adjustment
root.solve()
print(int(root.number))
# for (n, m) in monkeys.items():
#     print(f"{n}: {m}")
