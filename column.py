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
    columns = int(columns)
    items = list(line.strip() for line in file)
    longest = max(map(len, items))
    return 0


def mainargs(argv=None):
    pser = argparse.ArgumentParser()
    a = pser.add_argument
    a('file', type=argparse.FileType('r'), default='-')
    a('-c', '--columns', default=DEFAULT_COLUMNS, help='output is formatted for a display `columns` wide ("auto" for terminal width)')
    a('-s', '--separator', default=',  ', help='string used to separate columns',
    a('-x', '--fillrows', dest='mode', const=Mode.ROWS, action='store_const')
    args = pser.parse_args(argv)
    return vars(args)

if __name__ == "__main__":
    sys.exit(main(**mainargs()))
