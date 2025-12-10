from dataclasses import dataclass
from adventofcode import AoC # type: ignore
from collections import deque
from scipy.optimize import linprog, OptimizeResult
import numpy as np
from numpy.typing import NDArray

@dataclass
class Board:
    buttons: list[tuple[int, ...]]
    lights: list[bool]
    lights_goal: list[bool]
    joltage: list[int]
    joltage_goal: list[int]

def parse_line(line: str) -> Board:
    line_groups = line.split()
    lights = [False for _ in line_groups[0][1:-1]]
    lights_goal = [True if i == "#" else False for i in line_groups[0][1:-1]]
    buttons = [tuple(map(int, i[1:-1].split(","))) for i in line_groups[1:-1]]
    joltage = [0] * len(lights)
    joltage_goal = list(map(int, line_groups[-1][1:-1].split(",")))
    return Board(buttons=buttons, lights=lights, lights_goal=lights_goal, joltage=joltage, joltage_goal=joltage_goal)

def apply_button(board: Board, button: tuple[int, ...]):
    for opt in button:
        board.lights[opt] = not board.lights[opt]

def button_to_vec(button: tuple[int, ...], length: int) -> list[int]:
    out: list[int] = [0] * length
    for item in button:
        out[item] = 1
    return out

def still_under(lst_a: tuple[int, ...], lst_b: tuple[int, ...]) -> bool:
    for i in range(len(lst_a)):
        if lst_a[i] > lst_b[i]:
            return False
    return True

def solve_circuit(board: Board) -> int:    
    goal = tuple(board.lights_goal) # copy
    start = tuple(board.lights) # copy
    
    # bfs here
    if start == goal:
        return 0
    
    queue = deque([(start, 0)])
    visited = {start}
    
    while queue:
        current_state, presses = queue.popleft()
        
        for button in board.buttons:
            new_state = list(current_state)
            for opt in button:
                new_state[opt] = not new_state[opt]
            new_state_tuple = tuple(new_state)
            
            if new_state_tuple == goal:
                return presses + 1
            
            if new_state_tuple not in visited:
                visited.add(new_state_tuple)
                queue.append((new_state_tuple, presses + 1))
    
    return -1 # something has gone wrong here

def solve_circuit_p2(board: Board) -> int:
    # thanks google and chatgpt for saving me here. wasn't gonna write a solver from scratch lol
    n_buttons: int = len(board.buttons)
    n_positions: int = len(board.joltage_goal)
    
    A_eq: NDArray[np.float64] = np.zeros((n_positions, n_buttons))
    for i, button in enumerate(board.buttons):
        vec: list[int] = button_to_vec(button, n_positions)
        A_eq[:, i] = vec
    
    b_eq: NDArray[np.float64] = np.array(board.joltage_goal, dtype=np.float64)
    
    c: NDArray[np.float64] = np.ones(n_buttons)
    
    bounds: list[tuple[float, None]] = [(0, None) for _ in range(n_buttons)]
    
    result: OptimizeResult = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    
    if result.success and result.x is not None:
        solution: NDArray[np.int64] = np.round(result.x).astype(np.int64)
        if np.allclose(A_eq @ solution, b_eq):
            return int(np.sum(solution))
    
    return -1

def part1(inp: str) -> str | int | None:
    return sum(solve_circuit(parse_line(line)) for line in inp.splitlines())


def part2(inp: str) -> str | int | None:
    return sum(solve_circuit_p2(parse_line(line)) for line in inp.splitlines())


aoc = AoC(part_1=part1, part_2=part2)
inp = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
expected_result = 7
aoc.assert_p1(inp, expected_result)
aoc.submit_p1()

expected_result = 33
aoc.assert_p2(inp, expected_result)
aoc.submit_p2()
