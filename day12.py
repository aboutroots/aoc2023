from audioop import mul
from itertools import zip_longest
from utils import file_to_lines
import re
import cProfile
from functools import wraps

cache = {}


# def memoize(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         s = kwargs.get("hidden_spring")
#         r = kwargs.get("rules")
#         key = (s, r)
#         # print(key)
#         if key in cache:
#             print("cache hit")
#         if key not in cache:
#             cache[key] = func(*args, **kwargs)
#         return cache[key]

#     return wrapper


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


def is_valid_hidden_spring(hidden_spring, pattern):
    return re.match(pattern, hidden_spring) is not None


def find_index_to_left(lst, curr_index, condition):
    for i in range(curr_index - 1, -1, -1):
        if condition(lst[i]):
            return i
    return None  # Return None if no matching element is found to the left


# @memoize
def generate_springs(
    hidden_spring, pattern_strict, pattern_hidden, req_n_hashes, group, rules
):
    unknown_index = hidden_spring.find("?")
    if unknown_index == -1:
        # print(hidden_spring, req_n_hashes, rules)
        if is_valid(hidden_spring, req_n_hashes, pattern_strict):
            print("valid!")
            return 1
        else:
            print("NOT valid")
            return 0

    ### magic
    # print()
    # print(hidden_spring, group)

    already_fixed_groups = [
        len(x) for x in hidden_spring.split("?")[0].split(".") if x != ""
    ]
    groups_left = []
    for idx, (a, b) in enumerate(zip_longest(already_fixed_groups, group)):
        if a != b:
            groups_left = group[idx:]
            break

    new_start_index = find_index_to_left(
        hidden_spring, unknown_index, lambda x: x == "."
    )
    if new_start_index is None:
        new_start_index = unknown_index
    else:
        new_start_index += 1

    # print(already_fixed_groups, group, groups_left)
    print("----------------------------------")
    print(new_start_index, unknown_index)
    print("{:>20}".format(hidden_spring))
    print("{:>20}".format(rules))
    print("already fixed {}".format(already_fixed_groups))
    print("left {}".format(groups_left))

    new_hidden_spring = (
        hidden_spring[new_start_index:unknown_index]
        + "X"
        + hidden_spring[unknown_index + 1 :]
    )
    print('new hidden spring "{}"'.format(new_hidden_spring))
    ###

    new_springs = 0

    for sign in [".", "#"]:
        new_spring = new_hidden_spring.replace("X", sign)
        new_pattern_hidden = get_pattern_groups_hidden(groups_left)
        # import ipdb

        # ipdb.set_trace()
        print(new_spring, new_pattern_hidden)
        if is_valid_hidden_spring(new_spring, new_pattern_hidden):
            new_springs += generate_springs(
                hidden_spring=new_spring,
                pattern_strict=get_pattern_groups_strict(groups_left),
                pattern_hidden=new_pattern_hidden,
                req_n_hashes=sum(groups_left),
                group=groups_left,
                rules=",".join([str(x) for x in groups_left]),
            )
    return new_springs


def solve(rows):
    # profiler = cProfile.Profile()
    # profiler.enable()
    arrangements = 0
    multiplier = 1
    for idx, row in enumerate(rows):
        spring, rules = row.split(" ")
        rules = [int(x) for x in rules.split(",")] * multiplier
        spring = "?".join([spring] * multiplier)
        new_springs = generate_springs(
            hidden_spring=spring,
            pattern_strict=get_pattern_groups_strict(rules),
            pattern_hidden=get_pattern_groups_hidden(rules),
            req_n_hashes=sum(rules),
            group=rules,
            rules=",".join([str(x) for x in rules]),
        )
        print(idx, new_springs)
        arrangements += new_springs
    print(arrangements)
    # profiler.disable()

    # profiler.print_stats(sort="cumulative")


if __name__ == "__main__":
    print(solve(file_to_lines(day=12)))
