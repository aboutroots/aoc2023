from utils import file_to_lines, rotate_matrix_left, rotate_matrix_right
import json


def compute_weights(matrix):
    total = 0
    for row in matrix:
        for idx, elem in enumerate(row, start=1):
            if elem == "O":
                total += idx
    return total


def move_stones_right(row):
    """Try moving as far right as possible, starting with the rightmost stone"""

    length = len(row)
    for index_from_start in range(length):
        # go backwards
        index = length - index_from_start - 1
        elem = row[index]
        is_last_element = index == length - 1
        if elem == "O" and not is_last_element:
            next_possible_index = index
            for i in range(index + 1, length):
                if row[i] == ".":
                    next_possible_index = i
                else:
                    break
            if next_possible_index != index:
                # swap the stone with the empty space
                row[index], row[next_possible_index] = (
                    row[next_possible_index],
                    row[index],
                )
    return row


def move_matrix_stones_right(matrix):
    new_matrix = []
    for row in matrix:
        new_matrix.append(move_stones_right(row))
    return new_matrix


def move_stones(matrix, direction="right"):
    """Move the stones in the matrix in the given direction.

    Since I can only move stones right, I need to rotate the matrix accordingly
    """
    if direction == "east":
        return move_matrix_stones_right(matrix)
    if direction == "north":
        matrix = rotate_matrix_right(matrix)
        matrix = move_matrix_stones_right(matrix)
        matrix = rotate_matrix_left(matrix)
        return matrix
    if direction == "west":
        matrix = rotate_matrix_right(matrix, n=2)
        matrix = move_matrix_stones_right(matrix)
        matrix = rotate_matrix_left(matrix, n=2)
        return matrix
    if direction == "south":
        matrix = rotate_matrix_left(matrix)
        matrix = move_matrix_stones_right(matrix)
        matrix = rotate_matrix_right(matrix)
        return matrix
    assert False


def compute_load_on_north(matrix):
    new_matrix = rotate_matrix_right(matrix)
    return compute_weights(new_matrix)


def spin_matrix(matrix):
    for d in ["north", "west", "south", "east"]:
        matrix = move_stones(matrix, direction=d)
    return matrix


def solve(rows):
    matrix = [list(row) for row in rows]

    total_spins = 1000000000

    # we need to find cycles. After a certain number of operations, the matrix will
    # look the same as it did before. We need to find the first and second time
    # this happens, and then we can calculate the remaining operations
    known_matrices = set()
    repetition_index_first = None
    repetition_index_second = None

    for idx in range(total_spins):
        matrix = spin_matrix(matrix)
        a_hash = json.dumps(matrix)
        if a_hash in known_matrices and repetition_index_first is None:
            # we have found that the matrix is repeating, but we don't know
            # how long the cycle is yet
            repetition_index_first = idx
            known_matrices = set()

        if a_hash in known_matrices and repetition_index_first is not None:
            # now we know the length of a cycle
            repetition_index_second = idx
            break

        known_matrices.add(json.dumps(matrix))

    cycle_length = repetition_index_second - repetition_index_first
    remaining_cycles = (total_spins - repetition_index_second) % cycle_length - 1

    for idx in range(remaining_cycles):
        # spin the matrix the remaining number of times
        matrix = spin_matrix(matrix)

    print(compute_load_on_north(matrix))


if __name__ == "__main__":
    print(solve(file_to_lines(day=14)))
