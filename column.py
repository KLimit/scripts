#!/usr/bin/env python3
import argparse
import enum
from os import get_terminal_size
import sys


Mode = enum.Enum('Mode', ['COLUMNS', 'ROWS', 'TABLE'])


DEFAULT_COLUMNS = 80

def main(file, columns=80, separator='  ', mode=Mode.COLUMNS):
    if columns == 'auto':
        try:
            columns, _ = get_terminal_size(file)
        except OSError:
            columns = DEFAULT_COLUMNS
    # "columns" will refer to character cells
    columns = int(columns)
    items = list(line.strip() for line in file)
    longest = max(map(len, items))
    # "lanes" for the columns of items
    lanes = max_lanes(columns, longest, len(sep))
    return 0


def max_lanes(columns, longest, sep):
    """Calculate the most lanes possible.

    columns is number of (character) columns
    longest is length of the longest item
    sep is length of the separator
    """
    # columns as a function of longest, sep, and lanes is
    # columns = longest * lanes + sep * (lanes - 1)
    # solve for lanes
    # columns = longest*lanes + sep*lanes - sep
    # columns + sep = lanes * (longest + sep)
    # lanes = (columns + sep) / (longest + sep)
    # then, you just floor the number of lanes (ceil will violate columns)
    return floor((columns + sep) / (longest + sep))


def mainargs(argv=None):
    pser = argparse.ArgumentParser()
    a = pser.add_argument
    a('file', type=argparse.FileType('r'), default='-')
    a('-c', '--columns', default=DEFAULT_COLUMNS, help='output is formatted for a display `columns` wide ("auto" for terminal width)')
    a('-s', '--separator', default='  ', help='string used to separate columns',
    a('-x', '--fillrows', dest='mode', const=Mode.ROWS, action='store_const')
    args = pser.parse_args(argv)
    return vars(args)

if __name__ == "__main__":
    sys.exit(main(**mainargs()))
