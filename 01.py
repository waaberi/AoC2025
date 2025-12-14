from adventofcode import AoC # type: ignore

class SlowerRotatedCounter:
    def __init__(self):
        self.number = 50
    def move(self, dir: int = 1):
        self.number = (self.number + dir) % 100
        return self.number == 0
    def update(self, rot: str, hack: int | None = None): # ik this is a lazy solution
        m = -1 if rot[0] == "L" else 1
        comp = [self.move(m) for _ in range(int(rot[1:]))]
        return sum(comp) if hack else comp[-1]

def solver(inp: str, hack: int | None = None) -> str | int | None:
    counter = SlowerRotatedCounter()
    return sum([counter.update(rot, hack) for rot in inp.split()])

def part1(inp: str) -> str | int | None:
    return solver(inp)

def part2(inp: str) -> str | int | None:
    return solver(inp, 1)


aoc = AoC(part_1=part1, part_2=part2)

inp = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

expected_result = 3
aoc.assert_p1(inp, expected_result)
aoc.submit_p1()

expected_result = 6
aoc.assert_p2(inp, expected_result)
aoc.submit_p2()
