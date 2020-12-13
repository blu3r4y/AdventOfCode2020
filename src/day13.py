# Advent of Code 2020, Day 13
# (c) blu3r4y

import numpy as np

from functools import reduce
from collections import namedtuple

from aocd.models import Puzzle
from funcy import print_calls, lfilter

Data = namedtuple("Data", "earliest bids")


@print_calls
def part1(data):
    bids = lfilter(lambda e: isinstance(e, int), data.bids)

    # the id of the next bus we can catch
    bid = bids[np.argmax([data.earliest % i for i in bids])]
    # the timestamp at which we can board this bus
    board = data.earliest - (data.earliest % bid) + bid
    # the time we have to wait
    wait = board - data.earliest

    return bid * wait


@print_calls
def part2(data):
    constraints = [(t, mod) for t, mod in enumerate(data.bids) if isinstance(mod, int)]

    def _chinese_remainder_theorem(an: (int, int), bn: (int, int)) -> (int, int):
        """
        Given two moduli `(a1, n1)` and `(a2, n2)` solves the congruence equation
        of `x = a1 (mod n1)` and `x = a2 (mod n2)` for `x` by the Chinese Remainder Theorem
        (c) https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Case_of_two_moduli
        :param an: Represents `(a1, n1)`
        :param bn: Represents `(a2, n2)`
        :return: A congruence `(x, n1 * n2)`
        """
        (a1, n1), (a2, n2) = an, bn

        # Bézout's Identity holds if n1 and n2 are co-prime
        # m1*n1 + m2*n2 = 1 = gcd(n1, n2)
        g, m1, m2 = xgcd(n1, n2)
        assert g == 1

        # reduce a and b to a new constraint y = x (mod n1*n2)
        x = (a1 * m2 * n2) + (a2 * m1 * n1)
        return x, n1 * n2

    # solve the general case of the Chinese Remainder Theorem via reduction
    # (c) https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Existence_(constructive_proof)
    n, mod = reduce(_chinese_remainder_theorem, constraints)

    # retrieve the smallest possible integer for the final congruence
    smallest = mod - n % mod
    return smallest


def xgcd(a: int, b: int) -> (int, int, int):
    """
    Applies the Extended Euclidean Algorithm which
    returns `(g, x, y)` such that `ax + by = g = gcd(a, b)`
    (c) https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
    """
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def load(data):
    lines = data.splitlines()
    return Data(earliest=int(lines[0]),
                bids=[int(e) if e.isnumeric() else e
                      for e in lines[1].split(",")])


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=13)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
