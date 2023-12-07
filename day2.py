from utils import file_to_lines


def is_game_valid(game):
    return all(set_is_possible(s) for s in game)


def set_is_possible(rgb_tuple):
    return rgb_tuple[0] <= 12 and rgb_tuple[1] <= 13 and rgb_tuple[2] <= 14


def power_of_cubes(game):
    r, g, b = 0, 0, 0
    for a_set in game:
        r = max(r, a_set[0])
        g = max(g, a_set[1])
        b = max(b, a_set[2])
    return r * g * b


def parse_sets_from_line(line):
    right = line.strip().split(": ")[1]
    sets = right.split("; ")
    splitted_sets = [s.split(", ") for s in sets]

    def parse_set_to_tuple(a_set_of_cubes):
        color_dict = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for color_name in color_dict.keys():
            for draw in a_set_of_cubes:
                if color_name in draw:
                    color_dict[color_name] = int(draw.split(" ")[0])
                    break
        return color_dict["red"], color_dict["green"], color_dict["blue"]

    return [parse_set_to_tuple(s) for s in splitted_sets]


def solve(rows):
    result_1 = 0
    result_2 = 0
    for idx, row in enumerate(rows, start=1):
        game = parse_sets_from_line(row)
        result_1 += idx if is_game_valid(game) else 0
        result_2 += power_of_cubes(game)
    return result_1, result_2


if __name__ == "__main__":
    print(solve(file_to_lines(day=2)))
