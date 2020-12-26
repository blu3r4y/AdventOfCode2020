# Advent of Code 2020, Day 25
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, lmap

SUBJECT = 7
PRIME = 20201227


@print_calls
def part1(data):
    # brute-force the loop secrets
    value, loop = 1, 0
    while True:
        loop += 1
        value = (value * SUBJECT) % PRIME
        if value in data:
            break

    # get the other public key and compute the key
    other = data[0] if data[1] == value else data[1]
    key = encrypt(other, loop)
    return key


def encrypt(subject, loops):
    value = 1
    for _ in range(loops):
        value = (value * subject) % PRIME
    return value


def load(data):
    return lmap(int, data.splitlines())


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=25)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
