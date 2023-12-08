#!/usr/bin/env python3
import sys
import tomllib

import rich
print = rich.print

def main(input, watch):
    print(tomllib.load(input))


def mainargs(argv=None):
    import argparse
    pser = argparse.ArgumentParser()
    pser.add_argument(
        'input',
        type=argparse.FileType('rb'),
        default='-',
        nargs='?',
    )
    pser.add_argument(
        '-w',
        '--watch',
        help='watch the file for updates (poll-based, does not work w/ stdin)',
        action='store_true',
    )
    args = pser.parse_args(argv)
    print(args.input)
    if args.watch and (args.input.name == '<stdin>'):
        pser.error('Cannot use the "watch" option when reading from stdin')
    return vars(args)


if __name__ == "__main__":
    sys.exit(main(**mainargs()))
