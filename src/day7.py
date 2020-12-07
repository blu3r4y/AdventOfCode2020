# Advent of Code 2020, Day 7
# (c) blu3r4y

import networkx as nx

from aocd.models import Puzzle
from funcy import print_calls
from parse import parse

START = "shiny gold"


@print_calls
def part1(graph):
    return len(nx.ancestors(graph, START))


@print_calls
def part2(graph):
    def _count_bags(node):
        count = 1
        for succ in graph.successors(node):
            count += graph[node][succ]["number"] * _count_bags(succ)
        return count

    # count all the inner bags, but don't count the outermost (-1)
    return _count_bags(START) - 1


def load(data):
    def _parse_inner(text):
        return [parse("{number:d} {bag} bag", bag.removesuffix("s"))
                for bag in text.removesuffix(".").split(", ")]

    graph = nx.DiGraph()

    for line in data.split("\n"):
        parts = line.split(" bags contain ")
        for inner in _parse_inner(parts[1]):
            if inner is not None:
                graph.add_edge(parts[0], inner["bag"], number=inner["number"])

    return graph


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=7)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
