import sys
from sympy import symbols, solve, Eq
from sympy.parsing.sympy_parser import parse_expr

eq = sys.stdin.readline().rstrip()
expr = parse_expr(eq)
print(solve(expr))
# 40962717833337
# expr2 = parse_expr("2 + X")
# sol = solve(expr2)
# print(expr2)
# print(sol)

# H = symbols("H")
# sol = solve(eq)
# print(sol)
