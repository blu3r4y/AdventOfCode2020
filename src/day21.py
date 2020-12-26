# Advent of Code 2020, Day 21
# (c) blu3r4y

from collections import defaultdict
from typing import Union

from aocd.models import Puzzle
from funcy import print_calls, cat
from pyrecord import Record

Food = Record.create_type("Food", "ingredients", "allergens")
Result = Record.create_type("Result", "allergic")


@print_calls
def part1(foods):
    allergic = map_ingredients_to_allergens(foods)

    # number of ingredients in all foods that are definitely not allergic
    all_ingredients = cat(f.ingredients for f in foods)
    result = sum(ing not in allergic.keys() for ing in all_ingredients)
    return result


@print_calls
def part2(foods):
    allergic = map_ingredients_to_allergens(foods)

    # allergic ingredients, alphabetically sorted by the allergen
    return ",".join(ing for ing, alg in sorted(allergic.items(), key=lambda pair: pair[1]))


def map_ingredients_to_allergens(foods):
    # map each allergen to a list of food ingredients
    matrix: Union[dict[list], dict[set]] = defaultdict(list)
    for food in foods:
        for allergen in food.allergens:
            matrix[allergen].append(food.ingredients)

    # now build the intersection of food ingredients
    for allergen, candidates in matrix.items():
        matrix[allergen] = set.intersection(*map(set, candidates))

    # maps ingredients to their allergen
    allergic = dict()

    # reduce the list of ingredients until we have a 1:1 mapping
    removals = {None}
    while len(removals) > 0:
        removals.clear()

        # find the entries that already have a 1:1 mapping
        for allergen, candidates in matrix.items():
            if len(candidates) == 1:
                ing = next(iter(candidates))
                allergic[ing] = allergen
                removals.add(ing)

        # remove those from all the other sets
        for allergen, candidates in matrix.items():
            matrix[allergen] = candidates.difference(removals)

    return allergic


def load(data):
    foods = []
    for line in data.splitlines():
        ingredients, allergens = line.rstrip(")").split(" (contains ")
        foods.append(Food(set(ingredients.split()), set(allergens.split(", "))))

    return foods


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=21)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
