from math import e
import re
from utils import file_to_lines

direction_map = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}

slash_right_map = {">": "^", "<": "v", "^": ">", "v": "<"}

slash_left_map = {">": "v", "<": "^", "^": "<", "v": ">"}


def determine_next(foton, matrix):
    direction = foton[2]
    next_x, next_y = (
        foton[0] + direction_map[direction][0],
        foton[1] + direction_map[direction][1],
    )
    try:
        if next_x < 0 or next_y < 0:
            raise IndexError
        return next_x, next_y, matrix[next_y][next_x]
    except IndexError:
        return None, None, None


def get_next_fotons(
    foton, matrix, next_x=None, next_y=None, next_item=None, direction=None
):
    if next_x is None or next_y is None or next_item is None:
        next_x, next_y, next_item = determine_next(foton, matrix)
        if next_item is None:
            return []
        direction = foton[2]

    if next_item == ".":
        return [(next_x, next_y, direction)]

    if next_item == "/":
        return [(next_x, next_y, slash_right_map[direction])]

    if next_item == "\\":
        return [(next_x, next_y, slash_left_map[direction])]

    if next_item == "-":
        if direction in [">", "<"]:
            return [(next_x, next_y, direction)]
        else:
            return [(next_x, next_y, ">"), (next_x, next_y, "<")]
    if next_item == "|":
        if direction in ["^", "v"]:
            return [(next_x, next_y, direction)]
        else:
            return [(next_x, next_y, "^"), (next_x, next_y, "v")]


def compute_visited(known_fotons):
    visited_positions = set()
    for f in known_fotons:
        visited_positions.add((f[0], f[1]))
    return visited_positions


def get_start(matrix, point, direction):
    return get_next_fotons(
        foton=None,
        matrix=matrix,
        next_x=point[0],
        next_y=point[1],
        next_item=matrix[point[1]][point[0]],
        direction=direction,
    )


def solve_for_starting_point(matrix, point, direction):
    # known_fotons will not only hold the positions visited, but also the direction
    start_fotons = get_start(matrix, point, direction)
    known_fotons = set(start_fotons)
    fotons = start_fotons

    while len(fotons):
        # move fotons
        new_fotons = []
        for foton in fotons:
            new_fotons.extend(get_next_fotons(foton, matrix))
        fotons = [f for f in new_fotons if f not in known_fotons]
        known_fotons.update(set(fotons))

    # compute positions visited
    visited_positions = compute_visited(known_fotons)
    return len(visited_positions)


def solve(rows):
    matrix = [list(row) for row in rows]

    # find starting points on edges
    starting_positions = [
        *[(0, y, ">") for y in range(len(matrix))],
        *[(len(matrix) - 1, y, "<") for y in range(len(matrix))],
        *[(x, 0, "v") for x in range(len(matrix[0]))],
        *[(x, len(matrix[0]) - 1, "^") for x in range(len(matrix[0]))],
    ]
    starting_positions = set(starting_positions)
    return max(
        solve_for_starting_point(matrix, (p[0], p[1]), p[2]) for p in starting_positions
    )


if __name__ == "__main__":
    print(solve(file_to_lines(day=16)))
