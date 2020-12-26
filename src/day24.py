# Advent of Code 2020, Day 24
# (c) blu3r4y

from itertools import product
from collections import defaultdict

from aocd.models import Puzzle
from funcy import print_calls
from lark import Lark

# input grammar
DIRECTIONS_GRAMMAR = r"""
    ?start: direction*
    ?direction: "e"     -> e
        | "se"          -> se
        | "sw"          -> sw
        | "w"           -> w
        | "nw"          -> nw
        | "ne"          -> ne
"""

# encoding for white and black cells
WHITE, BLACK = 0, 1

# the 6 neighbours of a hex cell
OFFSETS = list(filter(lambda xy: xy[0] != xy[1],
                      product((-1, 0, +1), repeat=2)))


@print_calls
def part1(data):
    # number of black tiles after initialization
    tiles = initialize(data)
    return sum(tiles.values())


@print_calls
def part2(data, rounds=100):
    tiles = initialize(data)

    for _ in range(rounds):
        # identify the grid bounds (+1 to also investigate neighbours)
        xs, ys = zip(*tiles.keys())
        lox, hix = min(xs) - 1, max(xs) + 1
        loy, hiy = min(ys) - 1, max(ys) + 1

        flips = []

        # traverse entire visible grid
        for x in range(lox, hix + 1):
            for y in range(loy, hiy + 1):
                state = tiles[(x, y)]
                blacks = sum(neighbours(x, y, tiles))

                if state == BLACK and (blacks == 0 or blacks > 2):
                    flips.append((x, y))
                if state == WHITE and blacks == 2:
                    flips.append((x, y))

        # change all tiles at once
        for x, y in flips:
            flip(x, y, tiles)

    # number of black tiles after all rounds
    return sum(tiles.values())


def initialize(data):
    tiles = defaultdict(lambda: WHITE)
    for directions in data:
        x, y = 0, 0
        for direction in directions:
            x, y = move(x, y, direction)
        flip(x, y, tiles)

    return tiles


def flip(x, y, tiles):
    tiles[(x, y)] = BLACK if tiles[(x, y)] == WHITE else WHITE


def neighbours(x, y, tiles):
    return (tiles[(x + dx, y + dy)] for dx, dy in OFFSETS)


def move(x, y, direction):
    # move in hex coordinates
    # (c) http://devmag.org.za/2013/08/31/geometry-with-hex-coordinates/
    if direction == "e":
        x += 1
    elif direction == "se":
        x += 1
        y -= 1
    elif direction == "sw":
        y -= 1
    elif direction == "w":
        x -= 1
    elif direction == "nw":
        x -= 1
        y += 1
    elif direction == "ne":
        y += 1

    return x, y


def load(data):
    lark = Lark(DIRECTIONS_GRAMMAR)
    return [[token.data for token in lark.parse(line).children]
            for line in data.splitlines()]


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=24)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
