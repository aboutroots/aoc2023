from utils import file_to_lines


def parse_card(card):
    _, numbers = card.split(": ")
    winning, my = numbers.split(" | ")
    winning = [int(x) for x in winning.replace("  ", " ").strip().split(" ")]
    my = [int(x) for x in my.replace("  ", " ").strip().split(" ")]
    return my, winning


def solve(rows):
    result_1 = 0

    card_amounts = [1 for _ in range(len(rows))]

    for card_idx, card in enumerate(rows):
        my, winning = parse_card(card)
        subset_length = len(set(winning).intersection(set(my)))
        val = 2 ** (subset_length - 1) if subset_length > 0 else 0
        result_1 += val
        for _ in range(card_amounts[card_idx]):
            for i in range(card_idx + 1, card_idx + subset_length + 1):
                card_amounts[i] += 1

    print(result_1)

    print(sum(card_amounts))


if __name__ == "__main__":
    print(solve(file_to_lines(day=4)))
