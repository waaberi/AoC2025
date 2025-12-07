from adventofcode import AoC


def template(inp: str) -> tuple[list[list[str]], int]:
    lines = [list(line.lower()) for line in inp.splitlines()]
    i = 0
    splits = 0
    while i < len(lines) - 1:
        idx = 0
        while idx < len(lines[i]):
            if lines[i][idx] == "s":
                if lines[i+1][idx] == "^":
                    splits += 1
                    if 0 <= idx-1 < len(lines[i+1]): lines[i+1][idx-1] = "s"
                    if 0 <= idx+1 < len(lines[i+1]): lines[i+1][idx+1] = "s"
                else:
                    lines[i+1][idx] = "s"
            idx += 1
        i += 1
    return lines, splits

def part1(inp: str) -> str | int | None:
    _, splits = template(inp)
    return splits

def get_total_pathways(lst: list[list[str]], line: int, column: int, memo: dict[tuple[int, int], int]) -> int:
    if (line, column) in memo:
        return memo[(line, column)]
    if line == 0:
        return 1
    else:
        total = 0
        if line > 0 and lst[line-1][column] == "s":
            total += get_total_pathways(lst, line-1, column, memo)
        if column > 0 and lst[line-1][column-1] == "^":
            total += get_total_pathways(lst, line-2, column-1, memo)
        if column + 1 < len(lst[line-1]) and lst[line-1][column+1] == "^":
            total += get_total_pathways(lst, line-2, column+1, memo)
        memo[(line, column)] = total # someone could say, why not apply the memo in each if statement instead? well, doesn't make much of a difference bc it just means it'll get applied one layer earlier
        return total

def part2(inp: str) -> str | int | None:
    lines, _ = template(inp)
    total = 0
    memo: dict[tuple[int, int], int] = {}
    for i, elem in enumerate(lines[-1]):
        if elem == "s":
            total += get_total_pathways(lines, len(lines)-1, i, memo)

    return total



aoc = AoC(part_1=part1, part_2=part2)
inp = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
expected_result = 21
aoc.assert_p1(inp, expected_result)
aoc.submit_p1()

expected_result = 40
aoc.assert_p2(inp, expected_result)
aoc.submit_p2()
