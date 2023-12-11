from collections import Counter
from utils import file_to_lines


def get_type(hand):
    hand_list = list(hand)
    counter = Counter(hand_list)
    cards_value = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
    hand_value = [cards_value.index(card) for card in hand_list]

    if 5 in counter.values():
        # five of a kind
        return (6, *hand_value)
    elif 4 in counter.values():
        # four of a kind
        if "J" in hand_list:
            # we have five of a kind, (J + 4)
            return (6, *hand_value)
        return (5, *hand_value)
    elif 3 in counter.values() and 2 in counter.values():
        # full house
        if counter["J"] == 1:
            # we have four of a kind, (J + 3) + 1
            return (5, *hand_value)
        if counter["J"] >= 2:
            # we have five of a kind, (J + J + 3)
            return (6, *hand_value)
        return (4, *hand_value)
    elif 3 in counter.values():
        # three of a kind
        if "J" in hand_list:
            if counter["J"] >= 1:
                # we have four of a kind, (J + 3) + 1
                # or
                # we have four of a kind, (J + J + J + 1) + 1
                return (5, *hand_value)
        return (3, *hand_value)
    elif len([x for x in counter.values() if x == 2]) == 2:
        # two pairs
        if "J" in hand_list:
            if counter["J"] == 1:
                # we have full house, (2 + J) + 2
                return (4, *hand_value)
            if counter["J"] == 2:
                # we have four of a kind, (J + J + 2) + 1
                return (5, *hand_value)
        return (2, *hand_value)
    elif 2 in counter.values():
        # one pair
        if "J" in hand_list:
            if counter["J"] >= 1:
                # we have 3 of a kind, (2 + J) + 1 + 1
                # or
                # we have 3 of a kind, (J + J + 1) + 1 + 1
                return (3, *hand_value)
        return (1, *hand_value)
    else:
        # high card
        if "J" in hand_list:
            # we have one pair, (J + 1) + 1 + 1 + 1
            return (1, *hand_value)
        return (0, *hand_value)


def parse_hands(rows):
    hands = []
    for row in rows:
        hand, bid = row.split(" ")
        bid = int(bid.strip())
        hands.append((hand, bid, *get_type(hand)))
    return hands


def solve(rows):
    hands = parse_hands(rows)
    hands.sort(key=lambda hand: (hand[2], hand[3], hand[4], hand[5], hand[6], hand[7]))
    total_winnings = 0
    for idx, hand in enumerate(hands, start=1):
        hand_winnings = hand[1] * idx
        total_winnings += hand_winnings
    print(total_winnings)


if __name__ == "__main__":
    print(solve(file_to_lines(day=7)))
