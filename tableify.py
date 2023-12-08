#!/usr/bin/python3
"""Make a series of lines into a comma-separated table."""


import argparse
import fileinput
from itertools import zip_longest


def main(linesin, columns, delim):
    """Take the lines in, strip, join by delim and newlines by columns."""
    linesout = (
        delim.join(row) for row in zip_longest(
            *[(
                line.strip() for line in fileinput.input(linesin)
                if line.strip()
            )] * columns,
            fillvalue='',
        )
    )
    for line in linesout:
        print(line)


def args(argv=None):
    """Process the arguments for main."""
    pser = argparse.ArgumentParser()
    pser.add_argument(
        '-d',
        '--delimiter',
        dest='delim',
        default=',',
        help='delimiter for output (default is comma)',
    )
    pser.add_argument(
        'columns',
        type=int,
        help='number of columns to group into',
    )
    pser.add_argument(
        'linesin',
        default=None,
        nargs='*',
    )
    args = pser.parse_args(argv)
    return vars(args)


if __name__ == '__main__':
    main(**args())
