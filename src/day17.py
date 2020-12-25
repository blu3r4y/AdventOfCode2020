# Advent of Code 2020, Day 17
# (c) blu3r4y

from itertools import product
from collections import defaultdict

from aocd.models import Puzzle
from funcy import print_calls

INACTIVE, ACTIVE = 0, 1

# offsets for all 26 neighbours
OFFSETS3 = [xyz for xyz in product((-1, 0, +1), repeat=3)
            if not all(v == 0 for v in xyz)]

# offsets for all 80 neighbours
OFFSETS4 = [xyzw for xyzw in product((-1, 0, +1), repeat=4)
            if not all(v == 0 for v in xyzw)]


@print_calls
def part1(grid):
    return cycle(grid, dim=3)


@print_calls
def part2(grid):
    return cycle(grid, dim=4)


def cycle(grid, dim):
    # 3- or 4-dimensional variant
    neighbours = neighbours3 if dim == 3 else neighbours4

    for c in range(6):
        changes = []

        # apply the rule for each cell in the grid
        for xyz in product(range(-c - 4, c + 5), repeat=dim):
            state = grid[xyz]
            count = sum(neighbours(grid, *xyz))
            if state == ACTIVE and count not in (2, 3):
                changes.append((xyz, INACTIVE))
            if state == INACTIVE and count == 3:
                changes.append((xyz, ACTIVE))

        # apply changes
        for xyz, state in changes:
            grid[xyz] = state

    # number of active cells
    return sum(grid.values())


def neighbours3(grid, x, y, z):
    return (
        grid[(x + dx, y + dy, z + dz)]
        for (dx, dy, dz) in OFFSETS3
    )


def neighbours4(grid, x, y, z, w):
    return (
        grid[(x + dx, y + dy, z + dz, w + dw)]
        for (dx, dy, dz, dw) in OFFSETS4
    )


def load(data, dim):
    grid = defaultdict(lambda: INACTIVE)

    lines = data.splitlines()
    offset = (len(lines) - 1) // 2

    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            key = (x - offset, y - offset, 0) if dim == 3 else (x - offset, y - offset, 0, 0)
            grid[key] = ACTIVE if ch == "#" else INACTIVE

    return grid


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=17)

    ans1 = part1(load(puzzle.input_data, dim=3))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data, dim=4))
    # puzzle.answer_b = ans2
