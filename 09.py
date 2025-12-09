from adventofcode import AoC
import itertools

def is_top(prev: tuple[int, int], cur: tuple[int, int], next: tuple[int, int]):
    return cur[1] <= prev[1] and cur[1] <= next[1]

def is_left(prev: tuple[int, int], cur: tuple[int, int], next: tuple[int, int]):
    return cur[0] <= prev[0] and cur[0] <= next[0]

def get_boundary_points(dat: list[tuple[int, int]], dir: int = 1) -> list[tuple[int, int]]:
    """
    Depending on corner:
    top left: dx = -1, dy = -1
    top right: dx = +1, dy = -1
    bottom left: dx = -1, dy = +1
    bottom right: dx = +1, dy = +1
    """
    ans: list[tuple[int, int]] = []
    
    for i in range(len(dat)):
        previous = dat[i-1]
        current = dat[i]
        next = dat[(i+1)%len(dat)]
        dx = -dir if is_top(previous, current, next) else dir
        dy = -dir if is_left(previous, current, next) else dir

        
        x, y = current
        
        if len(ans) > 0:
            prev_boundary = ans[-1]
            option1 = (x+dx, y+dy)
            option2 = (x-dx, y-dy)
            
            if prev_boundary[0] == option1[0] or prev_boundary[1] == option1[1]: # option1 aligned with prev, so we continue
                ans.append(option1)
            else:
                ans.append(option2)
        else:
            ans.append((x+dx, y+dy)) # we just assume + first. IT MAY BE WRONG WHICH IS WHY WE NEED TO CALCULATE THINGS FOR BOTH DIRECTION MUTLIPLIERS
    
    return ans

def area(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    dx = abs(p2[0] - p1[0]) + 1
    dy = abs(p2[1] - p1[1]) + 1
    return dx * dy

def val_in_between(num: int, a: int, b: int) -> bool:
    if b < a:
        a, b = b, a

    return a < num < b

def point_in_polygon(point: tuple[int, int], boundary: list[tuple[int, int]], memo: dict[tuple[int, int], bool]) -> bool:
    if point in memo:
        return memo[point]
    
    px, py = point
    crossings = 0

    for i in range(int(boundary[-1][1] == boundary[0][1]), len(boundary), 2):
        b1 = boundary[i-1]
        b2 = boundary[i]
        
        # Check if the point's y-coordinate is strictly between the edge's y-coordinates
        if val_in_between(py, b1[1], b2[1]) and b1[0] > px:
            crossings += 1
    
    # odd number of crossings means the point is inside
    memo[point] = crossings % 2 == 1
    return crossings % 2 == 1

def line_in_polygon(p1: tuple[int, int], p2: tuple[int, int], boundary: list[tuple[int, int]]) -> bool:
    p1x, p1y = p1
    p2x, p2y = p2

    # check if the line crosses any boundary edge
    if p1x == p2x: # we're dealing with a vertical line
        for i in range(int(boundary[-1][1] != boundary[0][1]), len(boundary), 2):
            x1, y1 = boundary[i-1]
            x2, y2 = boundary[i]

            if val_in_between(y1, p1y, p2y) and val_in_between(p1x, x1, x2): # intersection with horizontal line
                return False
    else: # it's a horizontal line
        for i in range(int(boundary[-1][0] != boundary[0][0]), len(boundary), 2):
            x1, y1 = boundary[i-1]
            x2, y2 = boundary[i]

            if val_in_between(x1, p1x, p2x) and val_in_between(p1y, y1, y2): # intersection with vertical line
                return False

    return True

def is_valid_rectangle(p1: tuple[int, int], p2: tuple[int, int], boundary: list[tuple[int, int]], memo: dict[tuple[int, int], bool]) -> bool:
    dx = p2[0]-p1[0]
    dy = p2[1]-p1[1]
    p3 = (p1[0]+dx, p1[1])
    p4 = (p1[0], p1[1]+dy)

    points: list[tuple[int, int]] = [p1, p2, p3, p4]
    #print(points)

    for point in points:
        if not point_in_polygon(point, boundary, memo):
            return False

    for i in range(4): # for every line of the rectangle, you need to check whether its fully contained within a boundary
        start = points[i-1]
        finish = points[i]

        if not line_in_polygon(start, finish, boundary):
            return False
    
    return True

def part1(inp: str) -> str | int | None:
    dat: list[tuple[int, int]] = [tuple(map(int, i.split(","))) for i in inp.splitlines()] # type: ignore
    m = 0
    for comb in itertools.combinations(dat, 2):
        m = max(m, area(comb[0], comb[1]))
    return m
    

def part2(inp: str) -> str | int | None:
    dat: list[tuple[int, int]] = [tuple(map(int, i.split(","))) for i in inp.splitlines()] # type: ignore
    
    boundary = get_boundary_points(dat, -1)
    memo: dict[tuple[int, int], bool] = {}
    if not point_in_polygon(dat[0], boundary, {}):
        boundary = get_boundary_points(dat, 1)

    m = 0
    for p1, p2 in itertools.combinations(dat, 2): # comb could maybe made faster? actually no, technically there is no reason to eliminate them
        tmp = area(p1, p2)
        #print(tmp)
        if tmp > m and is_valid_rectangle(p1, p2, boundary, memo):
            m = tmp

    return m

aoc = AoC(part_1=part1, part_2=part2)
inp = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
expected_result = 50
aoc.assert_p1(inp, expected_result)
aoc.submit_p1()

expected_result = 24
aoc.assert_p2(inp, expected_result)
for _ in range(10):
    aoc.submit_p2()
