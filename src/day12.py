# Advent of Code 2020, Day 12
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls
from parse import parse


@print_calls
def part1(instructions):
    pos, ort = 0j, (1 + 0j)
    for ins in instructions:
        pos, ort = move(pos, ort, ins["act"], ins["val"])
    return manhattan(pos)


@print_calls
def part2(instructions):
    spos, wpos = 0j, (10 + 1j)
    for ins in instructions:
        act, val = ins["act"], ins["val"]

        if act in ("N", "S", "E", "W"):
            wpos, _ = move(wpos, 0, act, val)
        elif act in ("L", "R"):
            _, wpos = move(0, wpos, act, val)
        elif act == "F":
            spos += wpos * val

    return manhattan(spos)


def move(pos, ort, act, val):
    if act == "N":
        pos += val * 1j
    elif act == "S":
        pos += val * -1j
    elif act == "E":
        pos += val * (1 + 0j)
    elif act == "W":
        pos += val * (-1 + 0j)
    elif act == "L":
        ort *= 1j ** (val // 90)
    elif act == "R":
        ort *= 1j ** (4 - val // 90)
    elif act == "F":
        pos += ort * val
    return pos, ort


def manhattan(pos):
    return int(abs(pos.real) + abs(pos.imag))


def load(data):
    return [parse("{act:l}{val:d}", line).named
            for line in data.split("\n")]


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=12)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
