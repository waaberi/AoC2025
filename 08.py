from adventofcode import AoC
import math
from itertools import combinations
from collections import Counter

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x: int):
        if (x == self.parent[x]): return x
        self.parent[x] = self.find(self.parent[x]) # path compression
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # already in same circuit
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

def dist_compute(inp: str) -> tuple[int, list[tuple[int, ...]],list[tuple[float, int, int]]]:
    points = [tuple(map(int, i.split(","))) for i in inp.splitlines()]
    n = len(points)
    
    distances: list[tuple[float, int, int]] = []
    for i, j in combinations(range(n), 2):
        dist = math.dist(points[i], points[j])
        distances.append((dist, i, j))
    
    distances.sort()

    return n, points, distances

def part1(inp: str, num_connections: int = 1000) -> str | int | None:
    n, _, distances = dist_compute(inp)

    uf = UnionFind(n)
    connections_made = 0
    
    for _, i, j in distances:
        if connections_made >= num_connections:
            break
        uf.union(i, j)
        connections_made += 1

    circuit_sizes = Counter(uf.find(i) for i in range(n))
    
    largest = sorted(circuit_sizes.values(), reverse=True)[:3]
    
    return largest[0] * largest[1] * largest[2]


def part2(inp: str) -> str | int | None:
    n, points, distances = dist_compute(inp)

    uf = UnionFind(n)
    last_connection = (0, 0)
    
    for _, i, j in distances:
        if uf.find(i) != uf.find(j):
            last_connection = (i, j)
            uf.union(i, j)
            
            roots = set(uf.find(k) for k in range(n))
            if len(roots) == 1:
                break
    
    # return product of X coordinates of the last two connected junctions
    return points[last_connection[0]][0] * points[last_connection[1]][0]


aoc = AoC(part_1=part1, part_2=part2)
inp = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
expected_result = 40
aoc.assert_p1(inp, 40)
aoc.submit_p1()

expected_result = 25272
aoc.assert_p2(inp, expected_result)
aoc.submit_p2()
