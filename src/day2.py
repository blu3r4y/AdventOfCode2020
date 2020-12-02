# Advent of Code 2020, Day 2
# (c) blu3r4y

from parse import parse

from aocd.models import Puzzle
from funcy import print_calls


@print_calls
def part1(policies):
    valid = 0
    for p in policies:
        num = p["pass"].count(p["char"])
        if p["low"] <= num <= p["high"]:
            valid += 1
    return valid


@print_calls
def part2(policies):
    valid = 0
    for p in policies:
        if (p["pass"][p["low"] - 1] == p["char"]) \
                ^ (p["pass"][p["high"] - 1] == p["char"]):
            valid += 1
    return valid


def load(data):
    return [parse("{low:d}-{high:d} {char:l}: {pass:w}", line)
            for line in data.split("\n")]


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=2)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
