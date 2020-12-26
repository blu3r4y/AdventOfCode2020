# Advent of Code 2020, Day 22
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, lmap

PLAYER1, PLAYER2 = 0, 1


@print_calls
def part1(p1, p2):
    # play until one player has all the cards
    while len(p1) > 0 and len(p2) > 0:
        c1, c2 = p1.pop(0), p2.pop(0)
        staple = sorted((c1, c2), reverse=True)

        lead = p1 if c1 > c2 else p2
        lead.extend(staple)

    # determine winner's score
    winner = p1 if len(p1) > 0 else p2
    return score(winner)


@print_calls
def part2(p1, p2):
    def _recursive_combat(deck1, deck2):
        # deck history for this game
        history = {(tuple(deck1), tuple(deck2))}

        while len(deck1) > 0 and len(deck2) > 0:
            c1, c2 = deck1.pop(0), deck2.pop(0)

            # possibly decide the winner with a sub-game
            if len(deck1) >= c1 and len(deck2) >= c2:
                lead, _ = _recursive_combat(deck1[:c1], deck2[:c2])
            else:
                lead = PLAYER1 if c1 > c2 else PLAYER2

            # build the staple with the winners card on top
            staple = (c1, c2) if lead == PLAYER1 else (c2, c1)

            # assign the staple to the winner
            deck = deck1 if lead == PLAYER1 else deck2
            deck.extend(staple)

            # if any deck ordering occurred before
            # the game ends and player 1 wins instantly
            state = (tuple(deck1), tuple(deck2))
            if state in history:
                return PLAYER1, deck1
            history.add(state)

        # return winner and his deck
        winner = PLAYER1 if len(deck1) > 0 else PLAYER2
        return winner, deck1 if winner == PLAYER1 else deck2

    # determine winner's score
    _, winner_deck = _recursive_combat(p1, p2)
    return score(winner_deck)


def score(deck):
    return sum(card * (i + 1) for i, card
               in enumerate(reversed(deck)))


def load(data):
    return (lmap(int, block.splitlines()[1:])
            for block in data.split("\n\n"))


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=22)

    ans1 = part1(*load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(*load(puzzle.input_data))
    # puzzle.answer_b = ans2
