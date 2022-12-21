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


monkeys = []
dependencies = defaultdict(lambda: None)
for line in lines:
    sp = line.split()
    name = line[: line.index(":")]
    if len(sp) == 2:  # just a number, monkey
        num = int(line[line.index(" ") + 1 :])
        nm = Monkey(name, num, is_expr=False)
        monkeys.append(nm)
    else:  # it's a expr, get both pieces and op
        lhs, op, rhs = sp[1:]
        nm = Monkey(name, None, is_expr=True, lhs=lhs, rhs=rhs, op=op)
        # exprs[name] = f"{lhs} {op} {rhs}"
        dependencies[lhs] = nm
        dependencies[rhs] = nm
        monkeys.append(nm)

print("before")
for m in monkeys:
    print(m)
# get all numbers first
# check all things that depend on this monkey
for m in monkeys:
    if m.is_expr:
        continue
    # if this monkey is a dependency of another, plug in its value
    above = dependencies[m.name]
    if above is not None:
        if above.lhs == m.name:
            above.lhs = m.number
        elif above.rhs == m.name:
            above.rhs = m.number
        else:
            print("shouldnt be here!!!!")
        if type(above.lhs) is int and type(above.rhs) is int:
            result = eval(f"{above.lhs} {above.op} {above.rhs}")
            above.number = result
            above.is_expr = False
            above.lhs = None
            above.rhs = None
            above.op = None

print("after")
for m in monkeys:
    print(m)
