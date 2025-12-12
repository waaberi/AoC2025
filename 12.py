from adventofcode import AoC

def feasible(x: int, y: int, amount: int) -> int:
    return x*y >= amount*8.1

def part1(inp: str) -> str | int | None:
    total = 0
    shapes: list[list[str]] = []
    for shape in inp.split("\n\n"):
        if "x" in shape:
            break
        shapes.append(shape.splitlines()[1:])

    opts = inp.split("\n\n")[-1]
    for opt in opts.splitlines():
        area, more_opts = opt.split(": ")
        x, y = map(int, area.split("x"))
        #print(x, y, [int(i) for i in more_opts.split()], feasible(x, y, sum(int(i) for i in more_opts.split())))
        total += feasible(x, y, sum(int(i) for i in more_opts.split()))
    #print(opts)

    return total
def part2(inp: str) -> str | int | None:
    return None


aoc = AoC(part_1=part1, part_2=part2)
inp = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""
expected_result = 2
aoc.assert_p1(inp, expected_result)
aoc.submit_p1()