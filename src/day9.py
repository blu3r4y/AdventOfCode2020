# Advent of Code 2020, Day 9
# (c) blu3r4y

import numpy as np

from aocd.models import Puzzle
from funcy import print_calls


@print_calls
def part1(numbers):
    return walk(numbers)


@print_calls
def part2(numbers):
    invalid = walk(numbers)

    # just brute-force contiguous ranges
    for i in range(len(numbers)):
        the_sum = numbers[i]
        for j in range(i + 1, len(numbers)):
            the_sum += numbers[j]

            if the_sum == invalid:
                window = numbers[i:j + 1]
                assert window.sum() == the_sum
                return window.min() + window.max()

            # abort early if the sum is already too large
            if the_sum > invalid:
                break


def walk(numbers, preamble=25):
    windows = []

    # pre-fill valid number set
    for x in numbers[:preamble]:
        windows.append(set([x + y for y in numbers[:preamble] if x != y]))

    # check validity from now on
    for i, x in enumerate(numbers[preamble:]):
        if not any(x in win for win in windows):
            return x

        # advance the window one step
        windows.pop(0)
        windows.append(set([x + y for y in numbers[i + 1:i + preamble]]))

    return None


def load(data):
    return np.fromstring(data, dtype=int, sep="\n")


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=9)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
