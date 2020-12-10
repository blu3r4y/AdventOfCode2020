# Advent of Code 2020, Day 10
# (c) blu3r4y

from itertools import groupby

import numpy as np

from aocd.models import Puzzle
from funcy import print_calls, lmap, ilen, collecting
from sympy import tribonacci


@print_calls
def part1(jolts):
    # number of 1-step and 3-step differences multiplied
    bins = np.bincount(np.diff(jolts))
    return bins[1] * bins[3]


@print_calls
def part2(jolts):
    # product of permutations that each run
    # of 1-step differences allows for
    lengths = consecutive_lengths(jolts)
    perms = permutations(lengths)
    return np.prod(perms)


@collecting
def consecutive_lengths(arr):
    diffs = np.diff(arr)
    for group, values in groupby(diffs):
        if group == 1:
            yield ilen(values)


@np.vectorize
def permutations(n):
    return 1 if n < 2 else tribonacci(n + 1)


def load(data):
    jolts = lmap(int, data.split("\n"))
    jolts = [0] + jolts + [max(jolts) + 3]
    return sorted(jolts)


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=10)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
