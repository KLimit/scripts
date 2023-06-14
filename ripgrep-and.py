#!/usr/bin/env python3
"""Run ripgrep on a path with multiple patterns and require all matches exist.

Arguments not listed in help will be passed to ripgrep.
"""
from shutil import which
import subprocess


RIPGREP = which('rg')


def main(patterns, searchpath, show_missing, for_ripgrep):
    results = [rg(pattern, searchpath, for_ripgrep) for pattern in patterns]
    exitcode = 0 if all(result == 0 for result in results) else 1
    if show_missing:
        failedpatterns = [
            pattern for pattern, result
            in zip(patterns, results)
            if result != 0
        ]
        print('Did not match:')
        print('\n'.join(failedpatterns))
    return exitcode

def rg(pattern, searchpath, for_ripgrep):
    """Do rg for one pattern on the searchpath."""
    result = subprocess.run([RIPGREP] + for_ripgrep + [pattern, searchpath])
    return result.returncode


def mainargs(argv=None):
    import argparse
    pser = argparse.ArgumentParser(
        epilog=__doc__,
        allow_abbrev=False,
    )
    pser.add_argument(
        '--show-missing',
        help='print patterns that did not have a match, if any',
        action='store_true',
    )
    pser.add_argument(
        'patterns',
        metavar='pattern',
        help='pattern(s) to search for (ANDed)',
        nargs='+',
    )
    pser.add_argument('searchpath', help='path to search in/on')

    args, for_ripgrep = pser.parse_known_args(argv)
    toreturn = vars(args)
    toreturn.update({'for_ripgrep': for_ripgrep})
    return toreturn


if __name__ == "__main__":
    import sys
    sys.exit(main(**mainargs()))
