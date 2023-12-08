from calendar import c
from collections import defaultdict
from utils import file_to_lines



def get_adjacent(center_x, center_y, matrix, n=8):
    """N can be 4 or 8"""
    neighbours = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    if n == 8:
        neighbours = [
            (-1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
        ]

    for directions in neighbours:
        next_x = center_x + directions[0]
        next_y = center_y + directions[1]
        if next_x < 0 or next_y < 0:
            continue
        try:
            item_at_index = matrix[next_y][next_x]
        except IndexError:
            continue
        yield (next_x, next_y, item_at_index)


def is_valid_part(matrix, value):
    start_x, start_y = (
        value[0],
        value[1],
    )
    flag = False
    for y in range(start_y, start_y + 1):
        for x in range(start_x, start_x + len(str(value[2]))):
            for item_at_index in get_adjacent(x, y, matrix):
                if not item_at_index[2].isdigit() and item_at_index[2] != ".":
                    if item_at_index[2] == "*":
                        return item_at_index
                    flag = True
    return flag


def solve(rows):
    parts = set()
    non_parts = set()
    potential_gears = defaultdict(list)

    matrix = [list(row) for row in rows]

    for y, row in enumerate(matrix):
        for x, col in enumerate(row):
            is_digit = col.isdigit()
            is_beginning_of_number = is_digit and (x == 0 or not row[x - 1].isnumeric())
            if is_beginning_of_number:
                # find a whole number
                whole_number = f"{col}"
                next_x = x + 1
                while next_x < len(row) and row[next_x].isnumeric():
                    whole_number += f"{row[next_x]}"
                    next_x += 1
                whole_number = int(whole_number, 10)

                value = (x, y, whole_number)

                # check if it's a part
                is_valid = is_valid_part(matrix, value)
                if is_valid:
                    if isinstance(is_valid, tuple):
                        potential_gears[is_valid].append(value)

                parts.add(value) if is_valid_part(matrix, value) else non_parts.add(
                    value
                )

    print(sum([v[2] for v in parts]))

    result_2 = 0
    for gear in potential_gears.values():
        if len(gear) != 2:
            continue
        result_2 += gear[0][2] * gear[1][2]

    print(result_2)



if __name__ == "__main__":
    print(solve(file_to_lines(day=3)))
