from itertools import zip_longest
from utils import file_to_lines
import re
import cProfile


def ensure_order(input_string, pattern):
    return re.match(pattern, input_string) is not None


def is_valid(spring, req_n_hashes, pattern):
    # print('testing spring "{}"'.format(spring))
    testing_spring = "." + spring + "."
    if testing_spring.count("#") != req_n_hashes:
        return False

    if not ensure_order(testing_spring, pattern):
        return False

    return True


def get_pattern_groups_strict(rules):
    h = ["".join(["#"] * g) for g in rules]
    return "\.*" + "\.+".join(h) + "\.*"


def get_pattern_groups_hidden(rules):
    h = ["".join(["[#, \?]"] * g) for g in rules]
    return "[\., \?]*" + "[\., \?]+".join(h) + "[\., \?]*"


def get_known_groups_of_hashes(hidden_spring):
    result = []
    current_subgroup = 0
    for idx, elem in enumerate(hidden_spring):
        if elem == "?":
            if current_subgroup > 0:
                result.append(current_subgroup)
            return result, idx
        if elem == "#":
            current_subgroup += 1
        if elem == ".":
            if current_subgroup > 0:
                result.append(current_subgroup)
                current_subgroup = 0
    if current_subgroup > 0:
        result.append(current_subgroup)
    return result, idx


def is_valid_hidden_spring(hidden_spring, pattern):
    return re.match(pattern, hidden_spring) is not None


def generate_springs(
    hidden_spring, pattern_strict, pattern_hidden, req_n_hashes, group
):
    unknown_index = hidden_spring.find("?")
    if unknown_index == -1:
        if is_valid(hidden_spring, req_n_hashes, pattern_strict):
            return 1
        else:
            return 0

    new_springs = 0

    ##### add heuristic to choose the best option
    use_dot = True
    use_hash = True

    known_groups_of_hashes, q_idx = get_known_groups_of_hashes(hidden_spring)
    if len(known_groups_of_hashes) > len(group):
        return 0

    unfinished_group = False
    rules_remaining = []
    for known_group, rule in zip_longest(known_groups_of_hashes, group):
        if known_group != rule:
            rules_remaining.append(rule)

    # print(known_groups_of_hashes, group)
    for idx, rule in enumerate(known_groups_of_hashes):
        if group[idx] == rule:
            continue
        elif group[idx] > rule:
            unfinished_group = True

    # if unfinished group, next must be '#'
    use_dot = not unfinished_group

    if not unfinished_group and unknown_index > 0:
        prev_char = hidden_spring[unknown_index - 1]
        if prev_char == "#":
            use_hash = False
            # this means that we just finished a group, next must be '.'

    # first option:
    if use_hash:
        new_hidden_spring = (
            hidden_spring[:unknown_index] + "#" + hidden_spring[unknown_index + 1 :]
        )
        if is_valid_hidden_spring(new_hidden_spring, pattern_hidden):
            new_springs += generate_springs(
                new_hidden_spring, pattern_strict, pattern_hidden, req_n_hashes, group
            )
    # second_option
    if use_dot:
        new_hidden_spring = (
            hidden_spring[:unknown_index] + "." + hidden_spring[unknown_index + 1 :]
        )
        if is_valid_hidden_spring(new_hidden_spring, pattern_hidden):
            new_springs += generate_springs(
                new_hidden_spring, pattern_strict, pattern_hidden, req_n_hashes, group
            )
    return new_springs
    # return [x for x in new_springs if is_valid(x, rules)]


def solve(rows):
    profiler = cProfile.Profile()
    profiler.enable()
    arrangements = 0
    for idx, row in enumerate(rows):
        print(idx)
        spring, rules = row.split(" ")
        rules = [int(x) for x in rules.split(",")] * 5
        spring = "?".join([spring] * 5)
        new_springs = generate_springs(
            spring,
            get_pattern_groups_strict(rules),
            get_pattern_groups_hidden(rules),
            req_n_hashes=sum(rules),
            group=rules,
        )
        # print(idx, len(new_springs))
        arrangements += new_springs
    print(arrangements)
    profiler.disable()

    profiler.print_stats(sort="cumulative")


if __name__ == "__main__":
    print(solve(file_to_lines(day=12)))
