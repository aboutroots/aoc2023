from functools import reduce
from utils import file_to_lines


class Lens:
    def __init__(self, l, f=None):
        self.l = l
        self.f = f

    def __eq__(self, other):
        return self.l == other.l


def get_hash_value(step):
    return reduce(lambda acc, char: ((acc + ord(char)) * 17) % 256, step, 0)


def solve(rows):
    steps = rows[0].split(",")
    boxes = {get_hash_value(step.replace("-", "=").split("=")[0]): [] for step in steps}
    for step in steps:
        label = step.replace("-", "=").split("=")[0]
        box_number = get_hash_value(label)
        try:
            lens_index = boxes[box_number].index(Lens(label))
        except ValueError:
            lens_index = -1
        if "=" in step:
            # add or replace the lens
            focal_length = int(step.split("=")[1])
            if lens_index == -1:
                boxes[box_number].append(Lens(label, focal_length))
            else:
                boxes[box_number][lens_index].f = focal_length
        else:
            # remove the lens
            if lens_index != -1:
                boxes[box_number].pop(lens_index)

    # get power
    power = 0
    for box, lenses in boxes.items():
        for idx, lens in enumerate(lenses, start=1):
            power += (box + 1) * idx * lens.f
    return power


if __name__ == "__main__":
    print(solve(file_to_lines(day=15)))
