# Advent of Code 2020, Day 15
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, lmap, flip


@print_calls
def part1(numbers, end=2020):
    num = numbers[-1]
    for turn in range(len(numbers), end):
        if num in numbers[:-1]:
            pre = turn - numbers[::-1].index(num) - 1
            prepre = turn - numbers[pre - 1::-1].index(num) - 2
            num = pre - prepre
        else:
            num = 0

        numbers.append(num)

    return num


# part2() is just a more efficient version than part1() ...

@print_calls
def part2(numbers, end=30000000):
    # store previously seen numbers in a fast set
    seen = set(numbers[:-1])

    # store the indexes of previously seen numbers in a fast dict
    index = flip(dict(enumerate(numbers)))
    indexpre = {}

    # last and before-last numbers
    pre, prepre = numbers[-1], numbers[-1]

    for turn in range(len(numbers), end):
        # difference or zero
        pre = index[pre] - indexpre[pre] if pre in seen else 0

        # append number to history (with a log of 1)
        seen.add(prepre)
        prepre = pre

        # store the index of this number
        # and also carry over the lag 1 index of that
        old_index = index.get(pre, None)
        index[pre] = turn
        if old_index is not None:
            indexpre[pre] = old_index

    return pre


def load(data):
    return lmap(int, data.split(","))


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=15)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
