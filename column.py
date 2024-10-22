#!/usr/bin/env python3
from __future__ import annotations
import argparse
import enum
import itertools
from os import get_terminal_size
import sys


def main(file, columns: int|str, separator: str, mode: Mode, just: Justify):
    if mode is None:
        mode = Mode.LANES
    if columns == 'auto':
        try:
            columns, _ = get_terminal_size(file)
        except OSError:
            columns = DEFAULT_COLUMNS
    # "columns" will refer to character cells
    columns = int(columns)
    try:
        just = just.value
    except AttributeError:
        just = Justify[just.upper()].value
    items = list(line.strip() for line in file)
    longest = max(map(len, items))
    lanes = max_lanes(columns, longest, len(separator))
    # short-circuit when all your items fit in the same row
    if lanes > len(items):
        table = [items]
    else:
        if isinstance(mode, str):
            mode = Mode[mode.upper()]
        table = mode(items, lanes)
    # table = list(table)
    # breakpoint()
    print_table(table, separator, just, longest)
    return 0


def rows_first(items, num_lanes):
    """Group items into rows of num_lanes lanes, filling rows first."""
    # easier to implement (see more_itertools.grouper)
    iterators = [iter(items)] * num_lanes
    return itertools.zip_longest(*iterators, fillvalue='')


def lanes_first(items, num_lanes):
    """Group items into rows of num_lanes, filling lanes first."""
    # `ceil` is just `floor + 1` (and I don't want to import math)
    lines = len(items) // num_lanes + 1
    items = itertools.cycle(items)
    # TODO: finish


def print_table(table, separator, just, longest):
    """Print the iterable of iterables.

    >>> print_table(['abc', 'def', 'xyz'], ' | ', '<', 1)
    a | b | c
    d | e | f
    x | y | z
    """
    fill = ' '  # TODO: make this an option
    format = '{:' + f'{fill}{just}{longest}' + '}'  # "{: >9}".format(item)
    for line in table:
        print(separator.join(format.format(item) for item in line))


def max_lanes(columns, longest, sep_length):
    """Get the maximal number of lanes accomodated by columns.

    >>> max_lanes(9, 1, 0)
    9
    >>> max_lanes(9, 1, 1)  # (x.x.x.x.x)
    5
    >>> max_lanes(9, 1, 2)  # (x..x..x..)
    3
    >>> max_lanes(9, 2, 2)  # (xx..xx..)
    2
    """
    # columns = longest * lanes + sep_length * (lanes - 1)
    # columns = longest * lanes + sep_length * lanes - sep_length
    # col = lanes * (longest + sep) - sep
    # lanes = (col + sep) / (longest + sep)
    # if lanes is rounded/ceil'd up, won't respect columns limit
    return (columns + sep_length) // (longest + sep_length)


class Mode(enum.Enum):
    LANES = lanes_first
    ROWS = rows_first
    # TABLE = enum.auto()
class Justify(enum.Enum):
    LEFT = '<'
    RIGHT = '>'
    CENTER = '^'
DEFAULT_COLUMNS = 80


def mainargs(argv=None):
    pser = argparse.ArgumentParser()
    a = pser.add_argument
    a('file', type=argparse.FileType('r'), default='-')
    a('-c', '--columns', default=DEFAULT_COLUMNS, help='output is formatted for a display `columns` wide ("auto" for terminal width)')
    a('-s', '--separator', default='  ', help='string used to separate columns')
    a('-x', '--fillrows', dest='mode', const=Mode.ROWS, action='store_const')
    a('-j', '--justify', dest='just', choices=Justify, default=Justify.LEFT)
    args = pser.parse_args(argv)
    return vars(args)

if __name__ == "__main__":
    main(**mainargs())
