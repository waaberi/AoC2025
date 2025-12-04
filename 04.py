from adventofcode import AoC

def proper_check_adj_pos(lst: list[list[str]], i: int, j: int) -> int:
    ans = -1
    for a in range(max(0, i-1), min(i+2, len(lst))):
        for b in range(max(0, j-1), min(j+2, len(lst[0]))):
            ans += lst[a][b] == "@"
    return ans


def solver_lazy(dat: list[list[str]]) -> tuple[list[list[str]], int]:
    ans = 0
    cpy = [i[:] for i in dat]
    for i in range(len(dat)):
        for j in range(len(dat[i])):
            if dat[i][j] == "@" and proper_check_adj_pos(dat, i, j) < 4:
                ans += 1
                cpy[i][j] = "x"
    return cpy, ans

def part2_lazy(inp: str) -> int:
    dat = [list(i) for i in inp.splitlines()]
    total = 0
    dat, summary = solver_lazy(dat)
    while summary != 0:
        #print(summary)
        total += summary
        dat, summary = solver_lazy(dat)
    return total

def part1(inp: str) -> str | int | None:
    return solver([list(i) for i in inp.splitlines()])

def solver(dat: list[list[str]], modify: bool = False):
    ans = 0
    for i in range(len(dat)):
        for j in range(len(dat[i])):
            if dat[i][j] == "@" and proper_check_adj_pos(dat, i, j) < 4:
                ans += 1
                if modify: dat[i][j] = "x"
    return ans

def part2(inp: str) -> str | int | None:
    dat = [list(i) for i in inp.splitlines()]
    total = 0
    while (summary := solver(dat, True)) != 0:
        #print(summary)
        total += summary
    return total


aoc = AoC(part_1=part1, part_2=part2_lazy)
inp = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
expected_result = 13
aoc.assert_p1(inp, expected_result)
aoc.submit_p1()

expected_result = 43
aoc.assert_p2(inp, expected_result)
aoc.submit_p2()
