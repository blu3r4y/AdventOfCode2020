# Advent of Code 2020, Day 20
# (c) blu3r4y

import math

from scipy import signal

from typing import Dict, List, Set, Iterable, Tuple
from functools import reduce
from operator import mul

import numpy as np

from funcy import print_calls, lmap, lcat, lkeep, first, walk_values
from aocd.models import Puzzle
from pyrecord import Record
from parse import parse

# number of possible orientations of tiles
NUM_ORIENTS = 8

# border index mapping: left, right, up, down
BORDER_INDEXES = {(-1, 0): 0, (1, 0): 1, (0, -1): 2, (0, 1): 3}
OPPOSING_BORDER_INDEXES = {0: 1, 1: 0, 2: 3, 3: 2}

# the sea monster
SEA_MONSTER = ["                  # ",
               "#    ##    ##    ###",
               " #  #  #  #  #  #   "]

# stores a bit of hashed metadata for each tile
HashTile = Record.create_type("HashTile", "tile", "edges", "plugs", "neighbours")
TilePlacement = Record.create_type("TilePlacement", "orient", "dx", "dy")
Placement = Record.create_type("Placement", "positions", "orients")


@print_calls
def part1(tiles):
    tiles = preprocess(tiles)

    # multiply the ids of the corner pieces
    result = reduce(mul, corners(tiles), 1)
    return result


@print_calls
def part2(tiles):
    tiles = preprocess(tiles)
    image = assemble_image(tiles, identify_placement(tiles))

    # mask away the monster and count remaining sea waves ('#')
    mask_monster(image)
    return image.sum()


def mask_monster(image: np.ndarray):
    # get the sea monster sub-matrix
    monster_list = lmap(lambda line: [sym == "#" for sym in line], SEA_MONSTER)
    monster = np.flipud(np.array(monster_list, dtype=int))

    # the full pattern matches if the cell holds this target value
    target = monster.sum()
    target_spots, target_orient = None, None

    for o in range(NUM_ORIENTS):
        correlation = signal.correlate2d(orient(image, o), monster, mode="same", boundary="fill")
        maximum = np.amax(correlation)

        # check if we found one or more sea monster
        if maximum == target:
            target_spots = np.argwhere(correlation == maximum)
            target_orient = o
            break

    # correctly orient image
    image = orient(image, target_orient)

    # prepare an inverse mask and offsets
    mask = 1 - monster

    # monster offsets (because the correlation returns the center position)
    dx, dy = np.array(monster.shape) // 2
    width, height = monster.shape

    # mask away the monster
    for x, y in target_spots:
        x, y = x - dx, y - dy + 1
        image[x:x + width, y:y + height] *= mask


def assemble_image(tiles: Dict[int, HashTile], placement: Placement) -> np.ndarray:
    # identify the size of each tile (by taking any tile and checking)
    width, height = next(iter(tiles.values())).tile.shape
    assert width == height
    shp = width - 2  # -2 because we will remove the border

    # prepare a big canvas
    stack = int(math.sqrt(len(tiles)))
    image = np.zeros([shp * stack, shp * stack], dtype=int)

    # identify the relative offset before placing the tiles
    ranges = np.array(list(placement.positions.values()))
    dx = np.array(ranges)[:, 0].min()
    dy = np.array(ranges)[:, 1].min()

    # place tiles in the canvas
    for no, (x, y) in placement.positions.items():
        # orient the tile and do some mysterious flipping,
        # otherwise, it won't align properly with the other tiles
        tile = orient(tiles[no].tile, k=placement.orients[no])
        tile = np.rot90(np.fliplr(tile), 1)

        x, y = x - dx, y - dy
        image[shp * x:shp * (x + 1), shp * y:shp * (y + 1)] = borderless(tile)

    return image


def identify_placement(tiles: Dict[int, HashTile]) -> Placement:
    # figure out the placement and orientation of each tile in the final image

    # fix one corner tile in its original orientation
    start = corners(tiles)[0]

    # the position and orientation of each tile in the picture
    img_positions = {start: (0, 0)}
    img_orients = {start: 0}

    # and initialize the fringe with its non-none neighbouring tiles
    unplaced = set(lkeep(tiles[start].neighbours))

    # assembly all the tiles
    while len(unplaced) > 0:
        # pop any tile from the fringe (and also grab its neighbouring tiles)
        candidate = unplaced.pop()
        neighbours = set(lkeep(tiles[candidate].neighbours))

        # identify any of the already fixed tiles
        fixed = (neighbours & img_positions.keys()).pop()

        # figure out the placement of the candidate tile
        fixed_tile = orient(tiles[fixed].tile, k=img_orients[fixed])
        placement = identify_tile_placement(fixed_tile, tiles[candidate].tile)

        # place the candidate relative to the fixed tile
        x, y = img_positions[fixed]
        img_positions[candidate] = (x + placement.dx, y + placement.dy)
        img_orients[candidate] = placement.orient

        # add the candidate's neighbours for the next iterations
        new_neighbours = neighbours - img_positions.keys()
        unplaced.update(new_neighbours)

    return Placement(positions=img_positions, orients=img_orients)


def identify_tile_placement(fixed: np.ndarray, candidate: np.ndarray) -> TilePlacement:
    # brute-force all different locations and orientations of the candidate
    for (dx, dy), idx in BORDER_INDEXES.items():
        # identify the border on the fixed tile that we need to match against in this position
        fixed_border = borders(fixed)[idx]
        # ... and the index of the border on the opposing tile
        opposing = OPPOSING_BORDER_INDEXES[idx]

        # try orienting the candidate tile now
        for o in range(NUM_ORIENTS):
            candidate_border = borders(orient(candidate, o))[opposing]
            if np.array_equal(fixed_border, candidate_border):
                return TilePlacement(orient=o, dx=dx, dy=dy)


def corners(tiles: Dict[int, HashTile]) -> List[int]:
    # tiles that have exactly two non-matching edges must be corner tiles
    predicate = lambda pair: pair[1].neighbours.count(None) == 2
    return lmap(first, filter(predicate, tiles.items()))


def preprocess(tiles: Dict[int, np.ndarray]) -> Dict[int, HashTile]:
    def _create_hash_tile(tile: np.ndarray) -> HashTile:
        # just store the hashed borders and hash the plugs of each tile
        edges_ = lmap(hashed, edges(tile))
        plugs_ = hashed(plugs(tile))
        return HashTile(tile=tile, edges=edges_, plugs=plugs_, neighbours=[])

    def _compute_neighbours(no: int, hash_tiles: Dict[int, HashTile]) -> None:
        # the hash tile numbers, except this one
        other_nos = [i for i in hash_tiles.keys() if i != no]

        # identify how many matching tiles each edge has in this tile
        for e1, e2 in hash_tiles[no].edges:
            neighbours = []

            # check if this edge matches up with any of the other tile plugs
            for other in other_nos:
                other_plugs = hash_tiles[other].plugs
                if e1 in other_plugs or e2 in other_plugs:
                    neighbours.append(other)

            # fortunately, each edge has always only at most one matching tile pair
            assert len(neighbours) <= 1
            candidate = neighbours[0] if len(neighbours) > 0 else None

            # the number of matching tiles for this border index
            hash_tiles[no].neighbours.append(candidate)

    # first create the hash tiles, then, compute the edge match list
    result = walk_values(_create_hash_tile, tiles)
    for key in result.keys():
        _compute_neighbours(key, result)

    return result


def plugs(tile: np.ndarray) -> List[np.ndarray]:
    # the eight possible 1d borders for this tile
    # identified by the four borders and their flipped variants
    return lcat(edges(tile))


def edges(tile: np.ndarray) -> List[Tuple[np.ndarray]]:
    # the borders, as a tuple in their normal and flipped variant
    e1 = borders(tile)
    e2 = mirrored(e1)

    return list(zip(e1, e2))


def borders(tile: np.ndarray) -> List[np.ndarray]:
    # the four 1d border arrays: left, right, up, down
    return [tile[:, 0], tile[:, -1], tile[0, :], tile[-1, :]]


def borderless(tile: np.ndarray) -> np.ndarray:
    # remove the border
    return tile[1:-1, 1:-1]


def orient(tile: np.ndarray, k: int) -> np.ndarray:
    # on of the 8 possible orientations of this tile
    # where k=0 will return the original, unmodified tile
    assert 0 <= k <= NUM_ORIENTS - 1
    rot, flip = k % 4, k >= 4

    if flip:
        tile = mirrored(tile)
    return np.rot90(tile, k=rot)


def hashed(arr: Iterable[np.ndarray]) -> Set[int]:
    # consistent array hashing on iterables of arrays
    return set(hash(a.tobytes()) for a in arr)


def mirrored(arr):
    # consistent flipping logic (left to right)
    return np.fliplr(arr)


def load(data):
    tiles = {}
    for lines in map(str.splitlines, data.split("\n\n")):
        no = parse("Tile {:d}:", lines[0])[0]
        tile = lmap(lambda line: [sym == "#" for sym in line], lines[1:])
        tiles[no] = np.array(tile, dtype=int)
    return tiles


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=20)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2
