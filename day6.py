from utils import file_to_lines


def parse_races(rows):
    times = [x for x in rows[0].split(": ")[1].strip().split(" ") if x]
    distances = [x for x in rows[1].split(": ")[1].strip().split(" ") if x]
    return [(int(x), int(y)) for x, y in zip(times, distances)]


def get_winning_options_count(allowed_time, distance):
    winning_range_start = None
    winning_range_end = None
    for pressed_time in range(0, allowed_time):
        s = pressed_time * (allowed_time - pressed_time)
        if s > distance:
            winning_range_start = pressed_time
            break
    for pressed_time in range(allowed_time, 0, -1):
        s = pressed_time * (allowed_time - pressed_time)
        if s > distance:
            winning_range_end = pressed_time
            break

    return winning_range_end - winning_range_start + 1


def solve(rows):
    # for part 2, parse input manually (remove spaces)
    races = parse_races(rows)
    options_result = 1
    for race in races:
        options_result *= get_winning_options_count(*race)
    print(options_result)


if __name__ == "__main__":
    print(solve(file_to_lines(day=6)))
