from itertools import zip_longest
from venv import create
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
    for elem in hidden_spring:
        if elem == "?":
            # if current_subgroup > 0:
            #     result.append(current_subgroup)
            return result
        if elem == "#":
            current_subgroup += 1
        if elem == ".":
            if current_subgroup > 0:
                result.append(current_subgroup)
                current_subgroup = 0
    if current_subgroup > 0:
        result.append(current_subgroup)
    return result


def is_valid_hidden_spring(hidden_spring, pattern, req_n_hashes=None):
    if hidden_spring.count("#") > req_n_hashes:
        return False

    return re.match(pattern, hidden_spring) is not None


def find_index_to_left(lst, curr_index, condition):
    for i in range(curr_index - 1, -1, -1):
        if condition(lst[i]):
            return i
    return None  # Return 0 if not found


def generate_springs(
    hidden_spring,
    pattern_strict,
    pattern_hidden,
    req_n_hashes,
    group,
    level,
    prev_parts,
):
    print("{:>20}".format(hidden_spring), group)
    unknown_index = hidden_spring.find("?")
    if unknown_index == -1 or len(group) == 0:
        # print(" " * level, "return", "".join(prev_parts) + hidden_spring)
        # return 1
        if is_valid(hidden_spring, req_n_hashes, pattern_strict):
            print(" " * level, "valid", "".join(prev_parts) + hidden_spring)
            return 1
        else:
            return 0

    new_springs = 0

    ##### add heuristic to choose the best option
    use_dot = True
    use_hash = True

    known_groups_of_hashes = get_known_groups_of_hashes(hidden_spring)
    # if len(known_groups_of_hashes) > len(group):
    #     return 0

    unfinished_group = False
    rules_remaining = []
    for idx, (known_group, rule) in enumerate(
        zip_longest(known_groups_of_hashes, group)
    ):
        if known_group != rule:
            rules_remaining = group[idx:]
            break

    if len(rules_remaining) == 0:
        rules_remaining = group

    # # print(known_groups_of_hashes, group)
    # for idx, rule in enumerate(known_groups_of_hashes):
    #     if group[idx] > rule:
    #         unfinished_group = True

    # # if unfinished group, next must be '#'
    # use_dot = not unfinished_group

    # if not unfinished_group and unknown_index > 0:
    #     prev_char = hidden_spring[unknown_index - 1]
    #     if prev_char == "#":
    #         use_hash = False
    #         # this means that we just finished a group, next must be '.'

    # import ipdb

    # ipdb.set_trace()

    # find the new start index. This is the indeex that must be a first # in a group
    # of ### preceeding the unknown index
    new_start_index = find_index_to_left(
        hidden_spring, unknown_index, lambda x: x != "#"
    )
    if new_start_index is None:
        new_start_index = 0
    elif new_start_index != unknown_index:
        new_start_index += 1
    # print(new_start_index, unknown_index, hidden_spring)
    import ipdb

    # ipdb.set_trace()

    # first option:
    if use_hash:
        new_springs += create_new(
            "#",
            level,
            hidden_spring,
            unknown_index,
            rules_remaining,
            new_start_index,
            prev_parts,
        )
    # second_option
    if use_dot:
        new_springs += create_new(
            ".",
            level,
            hidden_spring,
            unknown_index,
            rules_remaining,
            new_start_index,
            prev_parts,
        )

        # print("invalid . ", new_hidden_spring, rules_remaining)
    return new_springs
    # return [x for x in new_springs if is_valid(x, rules)]


def create_new(
    c, level, hidden_spring, unknown_index, rules_remaining, new_start_index, prev_parts
):
    new_hidden_spring = (
        hidden_spring[new_start_index:unknown_index]
        + c
        + hidden_spring[unknown_index + 1 :]
    )
    prev_part = hidden_spring[:new_start_index]
    # print(
    #     " ",
    #     " " * (len(hidden_spring) - len(new_hidden_spring)),
    #     new_hidden_spring,
    # )
    new_pattern_hidden = get_pattern_groups_hidden(rules_remaining)
    new_pattern_strict = get_pattern_groups_strict(rules_remaining)
    new_req_n_hashes = sum(rules_remaining)
    print(new_hidden_spring)
    if is_valid_hidden_spring(new_hidden_spring, new_pattern_hidden, new_req_n_hashes):
        # print("valid", new_hidden_spring)
        # print(
        #     " " * level,
        #     'new hidden spring # "{}"'.format(new_hidden_spring),
        #     rules_remaining,
        # )
        # if new_hidden_spring == "##??":
        #     ipdb.set_trace()
        if c == "#" and rules_remaining and rules_remaining[0] == 1:
            rules_remaining = rules_remaining[1:]
        return generate_springs(
            new_hidden_spring,
            new_pattern_strict,
            new_pattern_hidden,
            new_req_n_hashes,
            rules_remaining,
            level + 1,
            [*prev_parts, prev_part],
        )
    else:
        pass
        # print("invalid # ", new_hidden_spring, rules_remaining)
        return 0


def solve(rows):
    profiler = cProfile.Profile()
    profiler.enable()
    arrangements = 0
    multiplier = 1
    for idx, row in enumerate(rows):
        spring, rules = row.split(" ")
        rules = [int(x) for x in rules.split(",")] * multiplier
        spring = "?".join([spring] * multiplier)
        new_springs = generate_springs(
            spring,
            get_pattern_groups_strict(rules),
            get_pattern_groups_hidden(rules),
            req_n_hashes=sum(rules),
            group=rules,
            level=0,
            prev_parts=[],
        )
        print(idx, new_springs)
        arrangements += new_springs
    print(arrangements)
    profiler.disable()

    # profiler.print_stats(sort="cumulative")


if __name__ == "__main__":
    print(solve(file_to_lines(day=12)))
