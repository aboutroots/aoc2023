from utils import file_to_lines


def differences_between_vals(a_list):
    return [a_list[i] - a_list[i - 1] for i in range(1, len(a_list))]


def solve(rows):
    final_values_each_row = []
    first_values_each_row = []
    rows = [[int(x) for x in row.split(" ")] for row in rows]
    for row in rows:
        differences_rows = [row]
        while not all([x == 0 for x in differences_rows[-1]]):
            differences_rows.append(differences_between_vals(differences_rows[-1]))

        # iterate backwards
        for i in range(len(differences_rows) - 1):
            curr_row = differences_rows[len(differences_rows) - i - 1]
            prev_row = differences_rows[len(differences_rows) - i - 2]
            prev_row.append(prev_row[-1] + curr_row[-1])
            prev_row.insert(0, prev_row[0] - curr_row[0])
        final_values_each_row.append(differences_rows[0][-1])
        first_values_each_row.append(differences_rows[0][0])

    print(sum(final_values_each_row))
    print(sum(first_values_each_row))


if __name__ == "__main__":
    print(solve(file_to_lines(day=9)))
