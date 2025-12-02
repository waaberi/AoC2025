from adventofcode import AoC

def repeated_n_times(s: str, n: int):
    division = len(s)//n
    slice = s[0:division]
    for i in range(division, len(s), division):
        if slice != s[i:i+division]: return False
    return True

def verify(s: str, m: int | None =None):
    for i in range(2, (m or len(s)) + 1):
        if len(s) % i == 0 and repeated_n_times(s, i): return True
    return False

def solver(inp: str, m: int | None =None) -> str | int | None:
    dat = inp.strip().split(",")
    ans = 0
    for order in dat:
        p1, p2 = map(int, order.split("-"))
        for i in range(p1, p2+1):
            if verify(str(i), m):
                ans += i
    return ans

def part1(inp: str) -> str | int | None:
    return solver(inp, 2)

def part2(inp: str) -> str | int | None:
    return solver(inp)

aoc = AoC(part_1=part1, part_2=part2)
inp = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,\
1698522-1698528,446443-446449,38593856-38593862,565653-565659,\
824824821-824824827,2121212118-2121212124"""
expected_result = 1227775554
aoc.assert_p1(inp, expected_result)
aoc.submit_p1()

expected_result = 4174379265
aoc.assert_p2(inp, expected_result)
aoc.submit_p2()
