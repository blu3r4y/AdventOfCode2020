# Advent of Code 2020, Day 23
# (c) blu3r4y

from collections import namedtuple

from aocd.models import Puzzle
from funcy import print_calls, lmap, pairwise

Data = namedtuple("Data", "nxt start end")


@print_calls
def part1(data):
    nxt = play(data.nxt, data.start, moves=100)

    # format the output string
    text, cup = "", 1
    while (cup := nxt.pop(cup, None)) is not None:
        text += str(cup)
    return text


@print_calls
def part2(data):
    # break the cycle again
    del data.nxt[data.end]

    # extend up to 1 million
    hi = max(data.nxt) + 1
    extension = range(hi, 1_000_000 + 1)
    data.nxt.update(pairwise(extension))

    # re-wire the extension and the cycle
    data.nxt[data.end] = hi
    data.nxt[1_000_000] = data.start

    nxt = play(data.nxt, data.start, moves=10_000_000)

    # multiply the two cup labels after the 1-labeled cup
    result = nxt[1]
    result *= nxt[result]
    return str(result)


def play(nxt, start, moves):
    # lowest and highest cup labels
    lo, hi, size = min(nxt), max(nxt), len(nxt)
    curr = start

    for _ in range(moves):
        # pick-up the next three cups, clock-wise
        p1 = nxt[curr]
        p2 = nxt[p1]
        p3 = nxt[p2]

        # find destination label by continuous subtraction
        # (and possibly roll-under if we get too low)
        dst = curr - 1
        while dst < lo or dst in {p1, p2, p3}:
            dst -= 1
            if dst < lo:
                dst = hi

        # cut out the pick-up first
        nxt[curr] = nxt[p3]

        # insert the pick-up at the destination
        cups_dst = nxt[dst]
        nxt[dst] = p1
        nxt[p3] = cups_dst

        # advance to the next current cup
        curr = nxt[curr]

    return nxt


def load(data):
    nums = lmap(int, data)
    start, end = nums[0], nums[-1]

    # map cup labels to their successor cup label (cyclic)
    nxt = {c0: c1 for c0, c1 in pairwise(nums)}
    nxt[end] = start

    return Data(nxt=nxt, start=start, end=end)


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=23)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
