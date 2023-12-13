from utils import file_to_lines, rotate_matrix_right


def check_if_valid_reflection(pattern, idx):
    lines_one_side = pattern[:idx]
    lines_one_side = lines_one_side[::-1]
    lines_other_side = pattern[idx:]

    total_differences = 0
    for line, other_line in zip(lines_one_side, lines_other_side):
        total_differences += get_difference_amount(line, other_line)
        if total_differences > 1:
            return False
    return total_differences == 1


def get_difference_amount(line1, line2):
    return sum([1 for c1, c2 in zip(line1, line2) if c1 != c2])


def get_reflection_top_down(pattern):
    reflection = None
    for idx, line in enumerate(pattern):
        last_line = pattern[idx - 1] if idx > 0 else None
        if last_line and get_difference_amount(line, last_line) < 2:
            if reflection is None:
                is_valid = check_if_valid_reflection(pattern, idx)
                if is_valid:
                    reflection = idx
                    break
    return reflection


def get_reflection(pattern):
    rh = get_reflection_top_down(pattern) or 0

    pattern_as_matrix = [list(row) for row in pattern]
    new_pattern = ["".join(x) for x in rotate_matrix_right(pattern_as_matrix)]

    rv = get_reflection_top_down(new_pattern) or 0
    direction = "v" if rv > rh else "h"
    mirror = rv if rv > rh else rh
    if rv == 0 and rh == 0:
        raise ValueError("no reflection found")
    return direction, mirror


def solve(patterns):
    patterns = [[row.strip() for row in pattern.split(" ")] for pattern in patterns]
    result = 0
    for pattern in patterns:
        direction, from_start = get_reflection(pattern)
        if direction == "v":
            result += from_start
        if direction == "h":
            result += 100 * from_start
    return result


if __name__ == "__main__":
    print(solve(file_to_lines(day=13, separate_with_empty=True)))
