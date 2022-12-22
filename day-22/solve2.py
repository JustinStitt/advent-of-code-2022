import sys
import re
from dataclasses import dataclass

lines = [line.rstrip() for line in sys.stdin.readlines()]
N = 4  # 50 for big

faces = []
