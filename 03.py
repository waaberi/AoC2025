from adventofcode import AoC # type: ignore

def gradual_pruning(s: str, m: int):
    start = s[-m:] #1
    for i in range(len(s) - m - 1, -1, -1):#n-m
        copy = start#1
        for j in range(m):#m
            copy = max(copy, s[i] + start[:j] + start[j+1:])#1+2+1+
        start = copy
    return int(start)

def part1(inp: str) -> str | int | None:
    return sum([gradual_pruning(battery, 2) for battery in inp.strip().split()])

def part2(inp: str) -> str | int | None:
    return sum([gradual_pruning(battery, 12) for battery in inp.strip().split()])

aoc = AoC(part_1=part1, part_2=part2)
inp = """987654321111111
811111111111119
234234234234278
818181911112111"""
expected_result = 357
aoc.assert_p1(inp, expected_result)
aoc.submit_p1()

expected_result = 3121910778619
aoc.assert_p2(inp, expected_result)
aoc.submit_p2()
