import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]

operations = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "LSHIFT": lambda x, y: x << y,
    "RSHIFT": lambda x, y: x >> y,
    "NOT": lambda x, y: 2**16 + ~x,
}

variables = {}


class Expr:
    def __init__(self, lhs=None, rhs=None, op=None, value=None):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
        self.value = value
        self.foo = lambda: -1
        if self.op is not None:
            for (k, v) in operations.items():
                if self.op == k:
                    self.foo = v

        if self.op == "NOT":
            self.rhs = "0"

    def solve(self):
        if self.value is not None:
            try:
                x = int(self.value)
                return x
            except:
                # go resolve dependency from variables
                return variables[self.value].solve()

        try:
            x = int(self.lhs)
            self.lhs = x
        except:
            self.lhs = variables[self.lhs].solve()

        try:
            x = int(self.rhs)
            self.rhs = x
        except:
            self.rhs = variables[self.rhs].solve()

        return self.foo(self.lhs, self.rhs)


for line in lines:
    toks = line.split()
    # form expression objects for each line
    if len(toks) == 3:  # direct assignment
        val, _, res = toks
        # check if integer
        variables[res] = Expr(value=val)
        continue
    # some operation
    if "NOT" in line:
        op, lhs, _, rhs = toks
        expr = Expr(lhs=lhs, rhs=rhs, op=op)
        variables[rhs] = expr
    else:
        lhs, op, rhs, _, res = toks
        expr = Expr(lhs=lhs, rhs=rhs, op=op)
        variables[res] = expr
        # x LSHIFT 2 -> f

for (k, v) in variables.items():
    print(f"{k=}: {v.solve()}")

print(variables["a"].solve())
