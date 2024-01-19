#!/usr/bin/env python3
from collections import defaultdict as DefaultDict
from collections.abc import Iterable


def main(inp, hint_lines, min_occurrences, require, remove, split, verbose):
    with inp:
        occurrences = DefaultDict(int)
        out_lines = []
        for line in inp.readlines(hint_lines):
            line = line.strip()
            line = line.split(split)
            # save a copy of these context lines
            out_lines.append(line)
            for token in line:
                # here's where we count occurrences
                occurrences[token] += 1
        if min_occurrences is None:
            # use the number of hint lines as the minimum number of occurrences,
            # but if we're using the whole file as context, you need to get the
            # number from the lenght of out_lines
            min_occurrences = len(out_lines) if hint_lines == -1 else hint_lines
        # pick tokens that are nonunique
        toremove = tuple(
            token
            for token, total in occurrences.items()
            if (
                min_occurrences <= total
                and not any(req in token for req in require)
            )
            or any(rem in token for rem in remove)
        )
        # gotta remember to do the out_lines first
        for line in out_lines:
            print(scrub(line, toremove))
        # now the remainder of the input
        for line in inp:
            line = line.strip()
            line = line.split(split)
            line = scrub(line, toremove)
            print(scrub(line, toremove))
    if verbose:
        print('token occurrences:')
        for key, item in sorted(occurrences.items(), key=lambda pair: pair[1]):
            print(f'\t{key}: {item}')
        print(f'filtered the following: {toremove}')
    return 0


def scrub(line: Iterable, toremove: Iterable, join: str = ' '):
    return join.join(token for token in line if token not in toremove)


def mainargs(argv=None):
    import argparse
    pser = argparse.ArgumentParser()
    pser.add_argument(
        "--hint-lines",
        type=int,
        help="number of lines to read to determine non-unique substrings",
        default=-1,
    )
    pser.add_argument(
        "-n",
        "--min-occurrences",
        type=int,
        help="minimum occurrences to count as non-unique (default: hint-lines)",
        default=None,
    )
    pser.add_argument(
        '--require',
        action='append',
        help='substrings that must not be filtered out',
        default=[],
    )
    pser.add_argument(
        '--remove',
        action='append',
        help='substrings that should be filtered if in a token despite count',
        default=[],
    )
    pser.add_argument(
        '-s',
        '--split',
        help='substring to split by',
    )
    pser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
    )
    pser.add_argument(
        "inp",
        type=argparse.FileType(),
        help="file to read ('-' to use stdin)",
    )

    args = pser.parse_args(argv)
    return vars(args)


if __name__ == "__main__":
    import sys
    sys.exit(main(**mainargs()))
