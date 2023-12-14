def file_to_lines(day, separate_with_empty=False, strip_lines=True):
    if day is None:
        raise AttributeError("you forgot about the day... again!")
    lines = []
    filename = f"inputs/{day}.txt"

    if not separate_with_empty:
        with open(filename, "r") as file:
            lines = file.readlines()
        return lines if not strip_lines else [line.strip() for line in lines]

    with open(filename, "r") as file:
        # row may consist of data from multiple lines
        current_row = []
        for line in file:
            line_stripped = line.strip()
            if len(line_stripped):
                current_row.append(line_stripped if strip_lines else line)
            else:
                # we found an empty line
                row_joined = " ".join(current_row)
                lines.append(row_joined)
                current_row = []

        # add the last missing row that had no chance of being added
        if len(current_row):
            row_joined = " ".join(current_row)
            lines.append(row_joined)

        return lines


def get_adjacent(center_x, center_y, matrix, n=8):
    """Get points adjacent to the given point on matrix. N can be 4 or 8

    :return: generator of tuples (x, y, value)
    """
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


def chunks(xs, n):
    """Split list into chunks of size n"""
    n = max(1, n)
    return (xs[i : i + n] for i in range(0, len(xs), n))


def transpose(matrix):
    """Transpose matrix"""
    transposed_matrix = [list(row) for row in zip(*matrix)]
    return transposed_matrix


def rotate_matrix_right(matrix, n=1):
    for _ in range(n):
        matrix = transpose(matrix)
        matrix = [list(reversed(row)) for row in matrix]
    return matrix


def rotate_matrix_left(matrix, n=1):
    for _ in range(n):
        matrix = [list(row) for row in zip(*matrix)]
        matrix = list(reversed(matrix))
    return matrix
