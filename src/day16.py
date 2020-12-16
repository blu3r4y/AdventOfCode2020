# Advent of Code 2020, Day 16
# (c) blu3r4y

from collections import defaultdict

import numpy as np
from aocd.models import Puzzle
from funcy import print_calls, lmap, lcat
from parse import parse


@print_calls
def part1(data):
    return discard(data)["invalid_field_sum"]


def discard(data):
    # just consider all ranges, ignoring the field association
    all_fields = lcat(data["fields"].values())

    invalid_entries = set()
    invalid_field_sum = 0

    for i, ticket in enumerate(data["nearby"]):
        for value in ticket:
            if not any(lo <= value <= hi for lo, hi in all_fields):
                invalid_field_sum += value
                invalid_entries.add(i)
                break

    # remove the invalid indexes in the nearby list
    for i in sorted(invalid_entries, reverse=True):
        del data["nearby"][i]

    return dict(invalid_field_sum=invalid_field_sum, nearby=data["nearby"])


@print_calls
def part2(data):
    # discard invalid entries first and save them in a matrix
    data["nearby"] = discard(data)["nearby"]
    tickets = np.array(data["nearby"])

    # for each field, identify the columns that could match it
    candidates = defaultdict(list)
    for field in data["fields"].keys():
        for col in range(tickets.shape[1]):
            (lo1, hi1), (lo2, hi2) = data["fields"][field]

            ok1 = np.logical_and((lo1 <= tickets[:, col]), (tickets[:, col] <= hi1))
            ok2 = np.logical_and((lo2 <= tickets[:, col]), (tickets[:, col] <= hi2))

            # check if all ranges would match this column
            if np.all(np.logical_or(ok1, ok2)):
                candidates[field].append(col)

    # the final ordering {field: column}
    final_order = {}

    # assign the fields, by always taking the only option (just one candidate)
    # and removing that option from all the other options
    while len(candidates) > 0:
        chosen_field, col = next((field, cols[0]) for field, cols in candidates.items() if len(cols) == 1)

        # we have only on candidate for this field
        final_order[chosen_field] = col
        del candidates[chosen_field]

        # remove that candidate from all the other lists
        for field in candidates.keys():
            if col in candidates[field]:
                candidates[field].remove(col)

    # take the product of all "departure" fields
    result = 1
    for field, col in final_order.items():
        if field.startswith("departure"):
            result *= data["yours"][col]

    return result


def load(data):
    blocks = data.split("\n\n")

    fields = [parse("{field}: {lo1:d}-{hi1:d} or {lo2:d}-{hi2:d}", line).named for line in blocks[0].splitlines()]
    fields = {e["field"]: [(e["lo1"], e["hi1"]), (e["lo2"], e["hi2"])] for e in fields}
    yours = lmap(int, blocks[1].splitlines()[1].split(","))
    nearby = [lmap(int, line.split(",")) for line in blocks[2].splitlines()[1:]]

    return dict(fields=fields, yours=yours, nearby=nearby)


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=16)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
