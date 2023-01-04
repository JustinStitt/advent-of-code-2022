import sys
from collections import defaultdict
from pickle import dump, load
import os
import time


use_pickle = "-p" in sys.argv


cutoff = 4000000
print(f"Using Cutoff = {cutoff}")
lines = [line.rstrip() for line in sys.stdin.readlines()]
# Sensor at x=2, y=18: closest beacon is at x=-2, y=15
# parallel
sensors = []
beacons = []
ranges = []


def getEmptyList():
    return list()


def main():
    global ranges
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

    def combineListOfRanges(listOfRanges):
        global cutoff
        listOfRanges.sort(key=lambda x: x[0])
        merged = []
        for current in listOfRanges:
            if current[0] < 0:
                current[0] = 0
            if current[1] > cutoff:
                current[1] = cutoff
            if not merged:
                merged.append(current)
            else:
                previous = merged[-1]
                if current[0] <= previous[1] + 1:
                    previous[1] = max(previous[1], current[1])
                else:
                    merged.append(current)
        return merged

    ranges = defaultdict(getEmptyList)
    print("zip part", flush=True)
    for (sensor, beacon) in zip(sensors, beacons):
        sx, sy = sensor
        bx, by = beacon
        dist = abs(sx - bx) + abs(sy - by)
        for _y in range(sy - dist, sy + dist + 1):
            leftover = dist - abs(_y - sy)
            xrange = [sx - leftover, sx + leftover]
            ranges[_y].append(xrange)

    print("combining ranges", flush=True)
    # print(ranges)
    for (ylevel, _ranges) in ranges.items():
        merged = combineListOfRanges(_ranges)
        ranges[ylevel] = merged
    # print(ranges)


def solve():
    # pickle ranges
    if not use_pickle:
        with open("ranges.pickle", "wb") as fd:
            print("Saving Ranges Pickle")
            dump(ranges, fd)

    prev = None
    print("sum check", flush=True)
    for ylevel in range(0, 4000000 + 1):
        amnt_of_x_used = sum([abs(x[1] - x[0]) for x in ranges[ylevel]])
        # if prev is not None and abs(prev - amnt_of_x_used) != 3:
        #     print("EUREKA")
        #     print(amnt_of_x_used, prev, ylevel)
        #     break
        if amnt_of_x_used != 4000000:
            print("EUREKA: ", ylevel, amnt_of_x_used)  # THIS FINDS THE YLEVEL
            break
        prev = amnt_of_x_used

    # REVERSE ENGINEER YLEVEL
    FOUND_Y = 3367718
    print(ranges[3367718])  # [[0, 2721113], [2721115, 4000000]]
    FOUND_X = 2721114
    # notice only 2721114 is missing in the range!
    # now!
    print(FOUND_X * cutoff + FOUND_Y)
    # GIVES ANSWER
    # 10884459367718
    # WOW THAT WAS CRAZY AND NOT THE INTENDED SOLUTION LOL


if __name__ == "__main__":
    if not use_pickle:
        main()
        solve()
    else:
        filename = "ranges.pickle"
        filetime = time.localtime(os.path.getmtime(filename))
        print(
            f"Loading Ranges Pickle (Last Modified: {time.strftime('%x %X', filetime)})..."
        )
        with open(filename, "rb") as fd:
            ranges = load(fd)
        print("Now Solving...")
        solve()
