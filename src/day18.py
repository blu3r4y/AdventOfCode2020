# Advent of Code 2020, Day 18
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls
from lark import Lark, Transformer

LARK_IMPORTS = r"""
    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

# left-to-right mathematics
LTR_GRAMMAR = r"""
    ?expr: atom | add | mul
    ?add: expr "+" atom
    ?mul: expr "*" atom
    ?atom: NUMBER | "(" expr ")"
""" + LARK_IMPORTS

# add-before-mul mathematics
ABM_GRAMMAR = r"""
    ?expr: mul
    ?add: atom | add "+" atom
    ?mul: add | mul "*" add
    ?atom: NUMBER | "(" mul ")"
""" + LARK_IMPORTS


class ExpressionTransformer(Transformer):
    NUMBER = int

    def mul(self, args):
        return args[0] * args[1]

    def add(self, args):
        return args[0] + args[1]


@print_calls
def solve(tasks):
    transformer = ExpressionTransformer()
    results = map(transformer.transform, tasks)
    return sum(results)


def load(data, grammar):
    lark = Lark(grammar, start="expr")
    return [lark.parse(line) for line in data.splitlines()]


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=18)

    ans1 = solve(load(puzzle.input_data, grammar=LTR_GRAMMAR))
    # puzzle.answer_a = ans1
    ans2 = solve(load(puzzle.input_data, grammar=ABM_GRAMMAR))
    # puzzle.answer_b = ans2
