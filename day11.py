from utils import file_to_lines, transpose


def expand_universe_at_coordinates(matrix):
    expanded_rows = []
    updated_matrix = [list(row) for row in matrix]
    for y, row in enumerate(updated_matrix):
        if all([v == "." for v in row]):
            expanded_rows.append(y)
    updated_matrix = transpose(updated_matrix)
    expanded_cols = []
    for y, row in enumerate(updated_matrix):
        if all([v == "." for v in row]):
            expanded_cols.append(y)
    return expanded_rows, expanded_cols


def solve(rows):
    space_extension_factor = 1000000
    matrix = [list(row) for row in rows]
    expanded_rows, expanded_cols = expand_universe_at_coordinates(matrix)

    coordinates = {}
    coordinate_idx = 1
    for idx_y, row in enumerate(matrix):
        for idx_x, col in enumerate(row):
            if col != ".":
                coordinates[coordinate_idx] = (idx_x, idx_y)
                coordinate_idx += 1

    distances = {}
    for idx_y, coordinate in enumerate(coordinates.keys()):
        for other_coordinate in list(coordinates.keys())[idx_y + 1 :]:
            x1, y1 = coordinates[coordinate]
            x2, y2 = coordinates[other_coordinate]
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            min_y = min(y1, y2)
            max_y = max(y1, y2)

            distance_x = abs(x1 - x2)
            distance_y = abs(y1 - y2)

            expanded_spaces_x = len(
                [space for space in expanded_cols if space > min_x and space < max_x]
            )
            extended_spaces_y = len(
                [space for space in expanded_rows if space > min_y and space < max_y]
            )

            distance_x += expanded_spaces_x * (space_extension_factor - 1)
            distance_y += extended_spaces_y * (space_extension_factor - 1)

            distances[(coordinate, other_coordinate)] = distance_x + distance_y
    print(sum(distances.values()))


if __name__ == "__main__":
    print(solve(file_to_lines(day=11)))
