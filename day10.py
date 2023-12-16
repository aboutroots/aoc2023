from utils import file_to_lines, find_elements_in_matrix, get_adjacent


def is_available_direction(val, next_val):
    valid_elements = {
        "F": ["|", "-"],
        "7": ["|", "-"],
        "J": ["|", "-"],
        "L": ["|", "-"],
        "-": ["F", "7", "J", "L"],
        "|": ["F", "7", "J", "L"],
    }
    return next_val in valid_elements[val]


def build_loop(matrix, start):
    # 1. determine what element is "S"
    attachments_to_start = [
        item
        for item in get_adjacent(
            start[0], start[1], matrix, n=4, predicate=lambda x: x != "."
        )
    ]
    assert len(attachments_to_start) == 2

    print(attachments_to_start)

    # 2. determine what direction is available to go from "S", always go
    # clockwise


def solve(rows):
    matrix = [list(row) for row in rows]
    start = list(find_elements_in_matrix(matrix, lambda x: x == "S"))[0]
    loop = build_loop(matrix, start)

    pass


if __name__ == "__main__":
    print(solve(file_to_lines(day=10)))
