from utils import file_to_lines

words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def solve(lines):
    result = []
    for line in lines:
        chars = list(line.strip())
        first = None
        last = None
        i = 0
        while i < len(chars):
            val = None
            try:
                # numeric
                val = int(chars[i])
            except ValueError:
                # text
                for word in words:
                    remaining_chars_len = len(chars[i:])
                    word_len = len(word)
                    if word_len > remaining_chars_len:
                        continue
                    if all(chars[i + j] == word[j] for j in range(len(word))):
                        val = words.index(word) + 1
                        break
            finally:
                i += 1
                if val:
                    if first is None:
                        first = val
                    last = val

        new_item = int(f"{first}{last}")
        result.append(new_item)
    return sum(result)


if __name__ == "__main__":
    print(solve(file_to_lines(day=1)))
