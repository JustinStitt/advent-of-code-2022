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

# y = 2_000_000
y = 10
print("Y is: ", y)

# for each spot in grid check if its closer to sensor than its closest in parallel array

# cheese
actuals = []
for (sensor, beacon) in zip(sensors, beacons):
    actual = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
    actuals.append(actual)


def inRangeOfSensor(x, y):
    global actuals, no_larger_than
    # if (x, y) in beacons or (x, y) in sensors:
    #     print("DEAD: ", x, y)
    #     return False
    # check against all sensors
    for idx in range(len(sensors)):
        actual = actuals[idx]
        ours = abs(x - sensors[idx][0]) + abs(y - sensors[idx][1])
        if ours <= actual:
            # print(f"Hit beacon at: {sensors[idx]}")
            # print(f"{x=}, {y=}")
            # print("here")
            return True
    # print("EUREKA ", x, " ", y, flush=True)
    return False


smallest_x = min(sensors, key=lambda x: x[0])[0]
largest_x = max(sensors, key=lambda x: x[0])[0]
largest_dist = max(actuals)
lower_bound = smallest_x - largest_dist
upper_bound = largest_x + largest_dist
# count = 0
# for x in range(lower_bound, upper_bound):
#     res = inRangeOfSensor(x)
#     if res is True:
#         count += 1


# no 5374697, 4968537

no_larger_than = 4000000
# no_larger_than = 20
print(f"{no_larger_than=}")


def getTuningFrequency(x, y):
    global no_larger_than
    return x * no_larger_than + y


total = no_larger_than**2
curr = 0
for x in range(0, no_larger_than + 1):
    for y in range(0, no_larger_than + 1):
        curr += 1
        if curr % 1_000_000 == 0:
            print("Progress: ", curr / total, flush=True)
        res = inRangeOfSensor(x, y)
        if res == False:
            print("FOUND IT: ", x, y)
            break
