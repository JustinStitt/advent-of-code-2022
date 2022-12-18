import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]

cubes = set()

for line in lines:
    x, y, z = line.split(",")
    cubes.add((int(x), int(y), int(z)))

# for every cube, check how many of its cubes are covered by another cube
total_area = len(cubes) * 6  # assume no overlaps, each overlap is minus 2


for cube in cubes:
    x, y, z = cube
    for delta in range(-1, 2):
        if delta == 0:
            continue
        dx = cube[0] + delta
        dy = cube[1] + delta
        dz = cube[2] + delta
        if (dx, y, z) in cubes:
            print(f"{dx=}, {y=}, {z=}")
            total_area -= 1
        if (x, dy, z) in cubes:
            total_area -= 1
        if (x, y, dz) in cubes:
            total_area -= 1

print(total_area)
