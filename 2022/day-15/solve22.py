import sys

lines = [line.rstrip() for line in sys.stdin.readlines()]
# Sensor at x=2, y=18: closest beacon is at x=-2, y=15
# parallel
sensors = []
beacons = []

for line in lines:
    sensor, beacon = line.split(":")
    # print(f"{sensor=}, {beacon=}")
    sx = sensor[sensor.index("x") + 2 : sensor.index(",")]
    sy = sensor[sensor.index("y") + 2 :]
    sx = int(sx)
    sy = int(sy)
    bx = beacon[beacon.index("x") + 2 : beacon.index(",")]
    by = beacon[beacon.index("y") + 2 :]
    bx = int(bx)
    by = int(by)

    sensors.append((sx, sy))
    beacons.append((bx, by))

big = 4000000


used = set()

for (sensor, beacon) in zip(sensors, beacons):
    actual = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])  # man. dist
    # assume all in x, then dec by one, move in by one
    sx, sy = sensor
    bx, by = beacon
    # start from top, work way down
    for _y in range(sy - actual, sy + actual + 1):
        leftover = actual - abs(_y - sy)
        xrange = range(sx - leftover, sx + leftover + 1)
        for currentx in xrange:
            used.add((currentx, _y))

print("done")
for __x in range(0, 20):
    for __y in range(0, 20):
        pos = (__x, __y)
        if pos in beacons:
            print("B", end="")
        elif pos in sensors:
            print("S", end="")
        elif pos in used:
            print("#", end="")
        else:
            surrounded = 0
            if (__x, __y - 1) in used:
                surrounded += 1
            if (__x, __y + 1) in used:
                surrounded += 1
            if (__x - 1, __y) in used:
                surrounded += 1
            if (__x + 1, __y) in used:
                surrounded += 1
            if surrounded == 4:
                print("🟥", end="")
            else:
                print(".", end="")
    print()
