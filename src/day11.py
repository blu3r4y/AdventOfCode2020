# Advent of Code 2020, Day 11
# (c) blu3r4y

from itertools import product

import numpy as np

from aocd.models import Puzzle
from funcy import print_calls, remove, ilen, nth, flatten, split_by, first, second


class TextGrid:
    def __init__(self, grid: np.ndarray):
        self.grid = grid
        self.ncols = grid.shape[0]
        self.nrows = grid.shape[1]

    def get(self, c, r):
        return self.grid[c, r]

    def set(self, c, r, value):
        self.grid[c, r] = value

    def count(self, value):
        return (self.grid == value).sum()

    def coords(self):
        return product(range(self.ncols), range(self.nrows))

    def starsplit(self, c, r, match):
        limit = max(self.ncols, self.nrows)
        return (self.tracesplit(c, r, o, limit, match) for o in range(8))

    def neighbors(self, c, r, match=None):
        elements = flatten(self.trace(c, r, i) for i in range(8))
        return elements if match is None else filter(lambda e: e in match, elements)

    def tracesplit(self, c, r, o, limit, match):
        return split_by(lambda e: e not in match, self.trace(c, r, o, limit))

    def trace(self, c, r, o, limit=1):
        dc, dr = TextGrid.orient(o)
        return (self.grid[c + dc * d, r + dr * d] for d in range(1, limit + 1)
                if 0 <= c + dc * d < self.ncols and 0 <= r + dr * d < self.nrows)

    def __repr__(self):
        return "\n".join(["".join(e) for e in self.grid.T.tolist()])

    @staticmethod
    def orient(i):
        return nth(i, filter(lambda cr: cr != (0, 0), product((-1, 0, +1), repeat=2)))

    @staticmethod
    def from_string(text: str):
        # bring the input into a shape with the origin in the UPPER LEFT corner and [col, row] indexing
        grid = np.fromiter(remove("\n", text), dtype=(np.unicode, 1)).reshape(-1, text.index("\n")).T
        return TextGrid(grid)


@print_calls
def part1(grid):
    changeset = [None]

    while len(changeset) > 0:
        changeset.clear()

        for c, r in grid.coords():
            val = grid.get(c, r)
            if val == "L" and ilen(grid.neighbors(c, r, match=["#"])) == 0:
                changeset.append((c, r, "#"))
            elif val == "#" and ilen(grid.neighbors(c, r, match=["#"])) >= 4:
                changeset.append((c, r, "L"))

        for change in changeset:
            grid.set(*change)

    return grid.count("#")


@print_calls
def part2(grid):
    changeset = [None]

    while len(changeset) > 0:
        changeset.clear()

        for c, r in grid.coords():
            val = grid.get(c, r)
            if val == "L" or val == "#":
                splits = grid.starsplit(c, r, match=["L", "#"])
                occupied = sum(first(second(split)) == "#" for split in splits)
                if val == "L" and occupied == 0:
                    changeset.append((c, r, "#"))
                if val == "#" and occupied >= 5:
                    changeset.append((c, r, "L"))

        for change in changeset:
            grid.set(*change)

    return grid.count("#")


def load(data):
    return TextGrid.from_string(data)


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=11)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
