from adventofcode import AoC # type: ignore
from collections import deque
from functools import cache

def create_graph(inp: str) -> list[tuple[str, str]]:
    lines = inp.splitlines()
    graph: list[tuple[str, str]] = []
    for line in lines:
        input, outputs = line.split(": ")
        for output in outputs.split():
            graph.append((input, output))
    return graph

def create_adjacency_list(inp: str) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    lines = inp.splitlines()
    d: dict[str, list[str]] = {}
    backwards_d: dict[str, list[str]] = {}
    for line in lines:
        input, outputs = line.split(": ")
        d[input] = outputs.split()
        for output in outputs.split():
            if output in backwards_d:
                backwards_d[output].append(input)
            else:
                backwards_d[output] = [input]
    return d, backwards_d

def bfs_reachable(start: str, adjacency_list: dict[str, list[str]]) -> set[str]:
    reachable: set[str] = set()
    queue = deque([start])
    reachable.add(start)
    
    while queue:
        node = queue.popleft()
        for neighbor in adjacency_list.get(node, []):
            if neighbor not in reachable:
                reachable.add(neighbor)
                queue.append(neighbor)
    
    return reachable


def prune_graph(
    adjacency_list: dict[str, list[str]], 
    backwards_adjacency_list: dict[str, list[str]], 
    start: str, 
    end: str
) -> dict[str, list[str]]:
    forward_reachable = bfs_reachable(start, adjacency_list)
    backward_reachable = bfs_reachable(end, backwards_adjacency_list)
    
    valid_nodes = forward_reachable & backward_reachable
    
    return {node: [dst for dst in adjacency_list.get(node, []) if dst in valid_nodes] for node in valid_nodes}


def part1(inp: str) -> str | int | None:
    graph = create_graph(inp)

    # find all paths from "you" to "out"
    # standard bfs

    queue = deque([("you", ["you"])])
    counter = 0

    while queue:
        current, path = queue.popleft()
        
        if current == "out":
            counter += 1
            continue
        
        for src, dst in graph:
            if src == current and dst not in path:
                queue.append((dst, path + [dst]))

    return counter


def part2(inp: str) -> str | int | None:
    adjacency_list, backwards_adjacency_list = create_adjacency_list(inp)
    
    pruned_adj = prune_graph(adjacency_list, backwards_adjacency_list, "svr", "out")
    valid_nodes = set(pruned_adj.keys())
    
    if "dac" not in valid_nodes or "fft" not in valid_nodes:
        return 0
    
    @cache
    def count_paths(node: str, seen_dac: bool, seen_fft: bool) -> int:
        if node == "out":
            return 1 if (seen_dac and seen_fft) else 0
        
        total = 0
        for neighbor in pruned_adj.get(node, []):
            new_dac = seen_dac or (neighbor == "dac")
            new_fft = seen_fft or (neighbor == "fft")
            total += count_paths(neighbor, new_dac, new_fft)
        return total
    
    return count_paths("svr", False, False)

aoc = AoC(part_1=part1, part_2=part2)
inp_part1 = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
expected_result = 5
aoc.assert_p1(inp_part1, expected_result)
aoc.submit_p1()

inp_part2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""
expected_result = 2
aoc.assert_p2(inp_part2, expected_result)
aoc.submit_p2()
