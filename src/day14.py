# Advent of Code 2020, Day 14
# (c) blu3r4y

from collections import namedtuple, defaultdict
from itertools import product

from aocd.models import Puzzle
from funcy import print_calls, collecting
from parse import parse

Assignment = namedtuple("Assignment", "addr val")
Masking = namedtuple("Masking", "zeros ones floats")


@print_calls
def part1(program):
    mask = None
    memory = defaultdict(int)

    for stmt in program:
        # activate the current mask
        if isinstance(stmt, Masking):
            mask = stmt
            continue

        # set ones, clear zeros, then store
        val = stmt.val
        val |= mask.ones
        val &= ~mask.zeros

        memory[stmt.addr] = val

    return sum(memory.values())


@print_calls
def part2(program):
    mask = None
    memory = defaultdict(int)

    for stmt in program:
        # activate the current mask
        if isinstance(stmt, Masking):
            mask = stmt
            continue

        # set ones, clear floating
        addr = stmt.addr
        addr |= mask.ones
        addr &= ~mask.floats

        # find all indexes of 1s in the original floating mask
        floats = reversed("{:036b}".format(mask.floats))
        indexes = [i for i, bit in enumerate(floats) if bit == "1"]

        # traverse all possible bit assignments
        for combination in product('01', repeat=len(indexes)):
            new_addr = addr
            for i, bit in zip(indexes, combination):
                if bit == "1":
                    new_addr |= 1 << i
                elif bit == "0":
                    new_addr &= ~(1 << i)

            # store the value at the new address
            memory[new_addr] = stmt.val

    return sum(memory.values())


@collecting
def load(data):
    for line in data.splitlines():
        if line.startswith("mask"):
            bits = parse("mask = {bits}", line)["bits"]
            zeros = bits.translate(bits.maketrans("01X", "100"))
            ones = bits.translate(bits.maketrans("01X", "010"))
            floats = bits.translate(bits.maketrans("01X", "001"))
            yield Masking(zeros=int(zeros, 2), ones=int(ones, 2), floats=int(floats, 2))
        elif line.startswith("mem"):
            stmt = parse("mem[{addr:d}] = {val:d}", line)
            yield Assignment(addr=stmt["addr"], val=stmt["val"])


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=14)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
