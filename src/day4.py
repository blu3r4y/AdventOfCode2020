# Advent of Code 2020, Day 4
# (c) blu3r4y

import re

from aocd.models import Puzzle
from funcy import print_calls

REQUIRED = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]


@print_calls
def part1(passports):
    num_valid = 0
    for pp in passports:
        if all([fld in pp for fld in REQUIRED]):
            num_valid += 1
    return num_valid


@print_calls
def part2(passports):
    num_valid = 0
    for pp in passports:
        if all([r in pp for r in REQUIRED]):
            byr = re.match(r"^\d{4}$", pp["byr"])
            iyr = re.match(r"^\d{4}$", pp["iyr"])
            eyr = re.match(r"^\d{4}$", pp["eyr"])
            hgt = re.match(r"^(\d+)(cm|in)$", pp["hgt"])
            hcl = re.match(r"^#[0-9a-f]{6}$", pp["hcl"])
            ecl = re.match(r"^(amb|blu|brn|gry|grn|hzl|oth)$", pp["ecl"])
            pid = re.match(r"^\d{9}$", pp["pid"])

            if byr and iyr and eyr and hgt and hcl and ecl and pid \
                    and (1920 <= int(byr[0]) <= 2002) \
                    and (2010 <= int(iyr[0]) <= 2020) \
                    and (2020 <= int(eyr[0]) <= 2030) \
                    and ((hgt[2] == "cm" and 150 <= int(hgt[1]) <= 193)
                         or (hgt[2] == "in" and 59 <= int(hgt[1]) <= 76)):
                num_valid += 1

    return num_valid


def load(data):
    # noinspection PyTypeChecker
    return [dict([pp.split(":") for pp in re.split(r"\s", line)])
            for line in data.split("\n\n")]


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=4)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
