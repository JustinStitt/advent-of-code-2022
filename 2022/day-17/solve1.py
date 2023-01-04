import sys
from dataclasses import dataclass

lines = [line.rstrip() for line in sys.stdin.readlines()]

WIDTH = 7
STARTING_X = 2
current_highest = 0  # starts at the floor

all_shapes = []


@dataclass
class Point:
    x: int
    y: int


class Shape:
    def __init__(self, points):
        self.points = points
        self.moves = iter(lines[0] * 100)

    def __repr__(self):
        return f"{self.points=}"

    def getHighestYPoint(self):
        global current_highest
        # technically the lowest but w/e
        ans = sorted(self.points, key=lambda x: x.y, reverse=True)[0].y
        current_highest = max(current_highest, ans)
        return ans

    def moveDown(self):
        global all_shapes
        ok = True
        for point in self.points:
            p = Point(point.x, point.y - 1)
            for shape in all_shapes:
                if shape == self:
                    continue
                if p in shape.points:
                    # print("hit other shape")
                    return False

        # make the adjustment
        if ok:
            for point in self.points:
                point.y -= 1
                if point.y == -1:
                    # print("HIT FLOOR!")
                    return False
        return ok

    def moveSideways(self):
        global all_shapes
        cmove = next(self.moves)
        dx = 1 if cmove == ">" else -1
        new_points = []
        for p in self.points:
            x, y = (p.x, p.y)
            # check if we would hit something
            new_points.append(Point(x + dx, y))

        for point in new_points:
            if point.x >= WIDTH or point.x < 0:
                return False
            for shape in all_shapes:
                if shape is self:
                    continue
                if point in shape.points:
                    return False  # something blocking

        # make the move
        for point in self.points:
            point.x += dx
        return True  # ok


def makeHBar() -> Shape:
    points = list()
    for x in range(STARTING_X, STARTING_X + 4):
        points.append(Point(x, current_highest + 4))
    return Shape(points)


def makeVBar() -> Shape:
    points = list()
    for y in range(current_highest + 4, current_highest + 3 + 5):
        points.append(Point(STARTING_X, y))
    return Shape(points)


def makeCross() -> Shape:
    points = list()
    points.append(Point(STARTING_X + 1, current_highest + 4))
    points.append(Point(STARTING_X + 1, current_highest + 5))
    points.append(Point(STARTING_X + 1, current_highest + 6))
    points.append(Point(STARTING_X, current_highest + 5))
    points.append(Point(STARTING_X + 2, current_highest + 5))
    return Shape(points)


def makeSquare() -> Shape:
    points = list()
    points.append(Point(STARTING_X, current_highest + 4))
    points.append(Point(STARTING_X + 1, current_highest + 4))
    points.append(Point(STARTING_X + 0, current_highest + 5))
    points.append(Point(STARTING_X + 1, current_highest + 5))
    return Shape(points)


def makeL() -> Shape:
    points = list()
    points.append(Point(STARTING_X, current_highest + 4))
    points.append(Point(STARTING_X + 1, current_highest + 4))
    points.append(Point(STARTING_X + 2, current_highest + 4))
    points.append(Point(STARTING_X + 2, current_highest + 5))
    points.append(Point(STARTING_X + 2, current_highest + 6))
    return Shape(points)


def printShape(shp: Shape):
    points = shp.points
    for r in range(10):
        for c in range(10):
            p = Point(c, r)
            if p in points:
                print("#", end="")
            else:
                print(".", end="")
        print()


def generateNextShape() -> Shape:
    idx = 0
    shapes = [makeHBar, makeCross, makeL, makeVBar, makeSquare]

    while 1:
        next_shape = shapes[idx % len(shapes)]()
        all_shapes.append(next_shape)
        yield next_shape
        idx += 1


shape_generator = generateNextShape()


def printCave():
    global all_shapes
    for y in range(current_highest + 3):
        for x in range(WIDTH):
            p = Point(x, y)
            f = False
            for shape in all_shapes:
                if p in shape.points:
                    f = True
            if f:
                print("#", end="")
            else:
                print(".", end="")

        print()
    print("=====")


def solve(shape):
    # move shape down until no more
    while 1:
        # get pushed by jet
        res = shape.moveSideways()
        if res is False:  # do nothing
            continue
        # try to move down
        dres = shape.moveDown()
        if dres is False:
            # print("came to rest")
            break  # done


count = 2022
for shape in shape_generator:
    if count <= 0:
        break
    if count % 100 == 0:
        print(f"{count / 2022 * 100}%")
    solve(shape)
    shape.getHighestYPoint()
    # print(current_highest)
    count -= 1

# printCave()
print(current_highest)
"""
#### (hbar)

.#.
### (cross)
.#.

..#
..# (L)
###

#
#   (vbar)
#
#

##  (square)
##
"""
