from utils import chunks, file_to_lines


def merge_intervals(intervals):
    if len(intervals) == 0:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for current_start, current_end in intervals[1:]:
        previous_start, previous_end = merged[-1]

        if current_start <= previous_end:
            merged[-1] = (previous_start, max(current_end, previous_end))
        else:
            merged.append((current_start, current_end))
    return merged


def transform_intervals(in_start, in_stop, rule_start, dest_start, delta):
    # x1 is always greater than x0, x3 is always greater than x2
    x0, x1 = in_start, in_stop
    x2, x3 = rule_start, rule_start + delta - 1

    # case1 : outside of rule range
    if x1 < x2 or x3 < x0:
        parts_no_effect = [(x0, x1)]
        part_with_effect = None

    # case2 : all inside of rule range
    if x0 >= x2 and x1 <= x3:
        parts_no_effect = []
        part_with_effect = (x0, x1)

    # case3 : right side is inside of rule range
    if x0 < x2 and x1 >= x2 and x1 <= x3:
        parts_no_effect = [(x0, x2 - 1)]
        part_with_effect = (x2, x1)

    # case4 : left side is inside of rule range
    if x0 >= x2 and x0 <= x3 and x1 > x3:
        parts_no_effect = [(x3 + 1, x1)]
        part_with_effect = (x0, x3)

    # case5 : our interval is bigger than rule range on both sides
    if x0 < x2 and x1 > x3:
        parts_no_effect = [(x0, x2 - 1), (x3 + 1, x1)]
        part_with_effect = (x2, x3)

    if part_with_effect is not None:
        transformed_range = (
            dest_start + (part_with_effect[0] - x2),
            dest_start + (part_with_effect[1] - x2),
        )
        return transformed_range, parts_no_effect
    return None, parts_no_effect


def apply_rules(input_interval, rules):
    rows = [
        [int(x) for x in row.strip().split(" ")]
        for row in rules.split("\n")[1:]
        if row != ""
    ]

    transformed_ranges = []
    non_transformed_ranges = [input_interval]
    # iterate over rules
    for destination_start, source_start, delta in rows:
        # our base intervals to be transformed can be changed with each rule
        new_non_transformed_ranges = []
        for to_be_transformed in non_transformed_ranges:
            # the interval can be divided into multiple parts, some of them
            # are already transformed, some of them are not and might be
            # transformed by another rules
            new_transformed_range, new_still_ranges = transform_intervals(
                to_be_transformed[0],
                to_be_transformed[1],
                source_start,
                destination_start,
                delta,
            )
            if new_transformed_range is not None:
                transformed_ranges.append(new_transformed_range)
            new_non_transformed_ranges.extend(new_still_ranges)

        non_transformed_ranges = new_non_transformed_ranges
    return [*transformed_ranges, *non_transformed_ranges]


def solve(maps):
    # second
    # instead of considering whole ranges, consider only boundaries
    seeds = [int(x) for x in maps[0].split(": ")[1].split(" ")]
    intervals = [(chunk[0], chunk[0] + chunk[1] - 1) for chunk in chunks(seeds, 2)]
    for a_map in maps[1:]:
        new_intervals = []
        for interval in intervals:
            result = apply_rules(interval, a_map)
            new_intervals.extend(result)

        new_intervals = merge_intervals(new_intervals)
        intervals = new_intervals
    print(min(intervals, key=lambda x: x[0])[0])


if __name__ == "__main__":
    print(solve(file_to_lines(day=5, separate_with_empty=True, strip_lines=False)))
