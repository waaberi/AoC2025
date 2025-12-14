from adventofcode import AoC # type: ignore
import typing

def prod(lst: typing.Iterable[int]) -> int:
    ans = 1
    for elem in lst:
        ans *= elem
    return ans

def part1(inp: str) -> int:
    lines = inp.splitlines()

    row_count = len(lines)
    line_len = len(lines[0])
    start = 0
    total = 0
    accumulator: list[int] = [0] * (row_count-1)
    operation = ""

    while start < line_len:
        if operation == "":
            operation = lines[row_count-1][start]
        for row in range(row_count-1):
            if lines[row][start].isdigit():
                accumulator[row] *= 10
                accumulator[row] += int(lines[row][start])

        next_op_check = start + 1 < line_len and lines[row_count-1][start+1] != " "
        final_op_check = start + 1 == line_len

        if next_op_check or final_op_check:
            total += (prod if operation == "*" else sum)(accumulator)
            operation = ""
            accumulator = [0] * (row_count-1)

        start += 1

    return total

def part2(inp: str) -> int:
    lines = inp.splitlines()

    row_count = len(lines)
    start = len(lines[0]) - 1
    total = 0
    accumulator: list[int] = []
    
    while start >= 0:
        tmp = 0

        for row in range(row_count-1):
            if lines[row][start].isdigit():
                tmp *= 10
                tmp += int(lines[row][start])

        accumulator.append(tmp)

        operation = lines[row_count-1][start]

        if operation != " ":
            total += (prod if operation == "*" else sum)(accumulator)
            accumulator = []
            start -= 1

        start -= 1
    return total


aoc = AoC(part_1=part1, part_2=part2)
inp = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
expected_result = 4277556
aoc.assert_p1(inp, expected_result)
aoc.submit_p1()

expected_result = 3263827
aoc.assert_p2(inp, expected_result)
aoc.submit_p2()
