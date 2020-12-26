# Advent of Code 2020, Day 19
# (c) blu3r4y

import re

from typing import Union

from aocd.models import Puzzle
from funcy import print_calls, lmap
from pyrecord import Record

Data = Record.create_type("Data", "rules", "messages")

# Terminal: match the symbol exactly
Terminal = Record.create_type("Terminal", "symbol")
# disjunction: match any of the children
Disjunction = Record.create_type("Disjunction", "children")
# sequence: match the children in order
Sequence = Record.create_type("Sequence", "children")
# at least once: match the children one or multiple times
AtLeastOnce = Record.create_type("AtLeastOnce", "children")


@print_calls
def part1(data):
    regex = regex_transform(data.rules)
    matches = [regex.match(msg) is not None for msg in data.messages]
    return sum(matches)


@print_calls
def part2(data, depth=20):
    # the new 8-rule can be deduced to a "at-least-once" syntax
    # 8: 42 | 42 8 -> 8: 42+
    data.rules[8] = AtLeastOnce([42])

    # the new 11-rule is not regular, but we can expand it a few ("depth") times ;)
    # 11: 42 31 | 42 11 31 -> 11: (42 31) | (42 42 31 31) | (42 42 42 31 31 31) | ...
    children = [Sequence([42] * rep + [31] * rep) for rep in range(1, depth)]
    data.rules[11] = Disjunction(children)

    return part1(data)


def regex_transform(rules):
    def _reduce_token(token: Union[int, Terminal, Disjunction, Sequence]):
        if isinstance(token, int):
            return _reduce_token(rules[token])
        elif isinstance(token, Terminal):
            return token.symbol
        elif isinstance(token, Disjunction):
            opt = map(_reduce_token, token.children)
            return "(" + "|".join(opt) + ")"
        elif isinstance(token, Sequence):
            seq = map(_reduce_token, token.children)
            return "".join(seq)
        elif isinstance(token, AtLeastOnce):
            seq = map(_reduce_token, token.children)
            return "(" + "".join(seq) + ")+"

    # recursively deduce the tokens into a valid regex
    pattern = r"^" + _reduce_token(0) + r"$"
    return re.compile(pattern)


def load(data):
    txt_rules, txt_messages = data.split("\n\n")

    # parse the rule block
    rules = {}
    for no, rhs in [e.split(": ") for e in txt_rules.splitlines()]:
        no = int(no)

        if rhs.startswith('"'):
            # parse a rule like >131: "b"<
            rules[no] = Terminal(rhs.replace('"', ""))
        else:
            # parse a rule like >88: 40< or >126: 16 130< or >98: 131 104 | 116 128<
            options = [Sequence(lmap(int, opt.split())) for opt in rhs.split("|")]
            rules[no] = Disjunction(options)

    # parse the message block
    messages = txt_messages.splitlines()

    return Data(rules, messages)


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=19)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
