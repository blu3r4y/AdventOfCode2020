# Advent of Code 2020, Day 1
# (c) blu3r4y

import numpy as np

from aocd.models import Puzzle
from itertools import product
from funcy import print_calls


@print_calls
def part1(data):
    for i, j in product(data, data):
        if i + j == 2020:
            return i * j


@print_calls
def part2(data):
    for i, j, k in product(data, data, data):
        if i + j + k == 2020:
            return i * j * k


def load(data):
    return np.fromstring(data, dtype=int, sep="\n")


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=1)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
