# Advent of Code 2020, Day 6
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, lmap


@print_calls
def part1(form):
    counts = [len(set().union(*group)) for group in form]
    return sum(counts)


@print_calls
def part2(form):
    counts = [len(group[0].intersection(*group)) for group in form]
    return sum(counts)


def load(data):
    return [lmap(set, group.split("\n")) for group in data.split("\n\n")]


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=6)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
