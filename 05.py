from adventofcode import AoC # type: ignore

"""
3-5 (5 - 3 + 1 = 3)
10-14 (14 - 10 + 1 = 5)
12-18 (only count from 15)
16-20
"""

def preprocess(inp: str) -> tuple[list[tuple[int, int]], list[int]]:
    lines = inp.splitlines()
    ranges: list[tuple[int, int]] = []
    i = 0
    while lines[i] != "":
        mmin, mmax = (int(e) for e in lines[i].split("-"))
        ranges.append((mmin, mmax))
        i += 1
    
    ranges.sort()
    nums = sorted([int(lines[n]) for n in range(i+1, len(lines))])
    return ranges, nums

def part1(inp: str) -> int:
    ranges, nums = preprocess(inp)

    rangeptr = count = 0

    for num in nums:
        while rangeptr < len(ranges):
            mmin, mmax = ranges[rangeptr]
            if mmin > num:
                break
            elif mmin <= num <= mmax:
                count += 1
                break
            rangeptr += 1
            
    return count

def part2(inp: str) -> int:
    ranges, _ = preprocess(inp)

    mmin = mmax = count = 0

    for i in range(len(ranges)):
        new_mmin, new_mmax = ranges[i]
        mmin = max(new_mmin, mmax+1)
        mmax = max(mmax, new_mmax)
        count += new_mmax - mmin + 1

    return count

aoc = AoC(part_1=part1, part_2=part2)
inp = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
expected_result = 3
aoc.assert_p1(inp, expected_result)
aoc.submit_p1()
expected_result = 14
aoc.assert_p2(inp, expected_result)
aoc.submit_p2()
