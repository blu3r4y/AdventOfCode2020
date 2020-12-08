# Advent of Code 2020, Day 8
# (c) blu3r4y

from enum import Enum
from typing import List
from collections import namedtuple

from aocd.models import Puzzle
from funcy import print_calls

Instruction = namedtuple("Instruction", "ins val")


class ExecState(Enum):
    RUNNING = 0
    END_OF_CODE = 1
    INFINITE_LOOP = 2


class Machine:
    def __init__(self, code: List[Instruction]):
        self.code = code
        self.acc, self.ip, self.history, self.state = None, None, None, None
        self.reset()

    def reset(self):
        self.acc = 0  # global accumulator
        self.ip = 0  # instruction pointer
        self.history = []  # history of interpreted instructions
        self.state = ExecState.RUNNING  # what ended the execution

    def run(self) -> int:
        self.reset()
        while self.check_state() == ExecState.RUNNING:
            self.history.append(self.ip)
            self.ip = self.interpret()
        return self.acc

    def interpret(self) -> int:
        ins = self.code[self.ip]
        if ins.ins == "acc":
            self.acc += ins.val
        elif ins.ins == "jmp":
            return self.ip + ins.val
        return self.ip + 1

    def check_state(self) -> ExecState:
        self.state = ExecState.RUNNING
        if self.ip in self.history:
            # terminate before we would re-interpret an instruction
            self.state = ExecState.INFINITE_LOOP
        if self.ip == len(self.code):
            # terminate if we reached the end of the code block
            self.state = ExecState.END_OF_CODE
        return self.state


@print_calls
def part1(data):
    return Machine(data).run()


@print_calls
def part2(data):
    for i in range(len(data)):
        machine = Machine(swap(data, i))
        machine.run()
        # only output result if we properly could end the program
        if machine.state == ExecState.END_OF_CODE:
            return machine.acc


def swap(data, i):
    data = data.copy()
    ins = data[i]

    # swap jmp <-> nop instructions only
    if ins.ins == "jmp":
        data[i] = Instruction("nop", ins.val)
    elif ins.ins == "nop":
        data[i] = Instruction("jmp", ins.val)

    return data


def load(data):
    code = []
    for line in data.split("\n"):
        pts = line.split(" ")
        ins, val = pts[0], int(pts[1])
        code.append(Instruction(ins=ins, val=val))
    return code


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=8)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
