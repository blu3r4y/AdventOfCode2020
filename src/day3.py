# Advent of Code 2020, Day 3
# (c) blu3r4y

import numpy as np

from aocd.models import Puzzle
from funcy import print_calls, lmap


@print_calls
def part1(data):
    return traverse(data, (3, 1))


@print_calls
def part2(data):
    result = traverse(data, (1, 1))
    result *= traverse(data, (3, 1))
    result *= traverse(data, (5, 1))
    result *= traverse(data, (7, 1))
    result *= traverse(data, (1, 2))
    return result


def traverse(arr, slope):
    num_trees = 0
    pos = np.array([0, 0])

    # traverse until we reach the bottom
    while pos[1] < arr.shape[1]:
        # retrieve element, but wrap around all axis
        element = arr[tuple(pos % arr.shape)]
        if element == "#":
            num_trees += 1
        pos += slope

    return num_trees


def load(data):
    # index with [x, y]
    return np.array(lmap(list, data.split("\n"))).T


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=3)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
