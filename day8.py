from itertools import cycle
from utils import file_to_lines
import numpy as np


def parse_rows(rows):
    instr = [int(x) for x in list(rows[0].replace("L", "0").replace("R", "1"))]
    a_map = {}
    for row in rows[2:]:
        key = row.split(" = ")[0]
        values = row.split(" = ")[1].strip("(").strip(")").split(", ")
        a_map[key] = values
    return instr, a_map


def solve_for_one(item, instr, a_map):
    step = 0
    while True:
        step += 1
        move = next(instr)
        next_item = a_map[item][move]
        if next_item.endswith("Z"):
            break
        item = next_item
    return step


def solve(rows):
    instr, a_map = parse_rows(rows)
    items = [item for item in a_map.keys() if item.endswith("A")]
    results = []
    for item in items:
        results.append(solve_for_one(item, cycle(instr), a_map))

    print(results)
    print(np.lcm.reduce(results))


if __name__ == "__main__":
    print(solve(file_to_lines(day=8)))
