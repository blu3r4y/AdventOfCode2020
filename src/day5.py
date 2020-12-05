# Advent of Code 2020, Day 5
# (c) blu3r4y

import numpy as np

from aocd.models import Puzzle
from funcy import print_calls


@print_calls
def part1(codes):
    return max(compute_sids(codes))


@print_calls
def part2(codes):
    sids = compute_sids(codes)

    # find the index where the difference
    # in the sorted list of sids is greater than 1
    ssids = np.array(sorted(sids))
    lags = np.diff(ssids)
    pos = np.argwhere(lags > 1)[0, 0]

    return ssids[pos] + 1


def compute_sids(codes):
    sids = []
    for code in codes:
        r = transform(code[:7], "F", "B")
        c = transform(code[-3:], "L", "R")
        sid = r * 8 + c
        sids.append(sid)
    return sids


def transform(code, lo, hi):
    # convert to binary and parse
    code = code.replace(lo, "0").replace(hi, "1")
    return int(code, 2)


def load(data):
    return data.split()


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=5)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
