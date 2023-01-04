import sys
from collections import defaultdict
from aocdebug.debug import debug

DEBUG = True
debug = debug if DEBUG else lambda _: 0

lines = [line.rstrip() for line in sys.stdin.readlines()]

for line in lines:
    pass
