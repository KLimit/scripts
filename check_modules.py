#!/usr/bin/env python3
import argparse
import importlib
from pathlib import Path
import sys

from more_itertools import collapse

# TODO: split the import trying into a subcommand, make another subcommand for
# listing the nodes of the whole module


def main(root, clear_cache, list, raise_):
    all_exceptions = []
    for module, path in all_modules(root):
        try:
            importlib.import_module(module)
            if clear_cache:
                importlib.invalidate_caches()
        except Exception as e:
            all_exceptions.append((e, path))
    if all_exceptions:
        exceptions, paths = zip(*all_exceptions)
        if raise_:
            raise ExceptionGroup('some imports failed', exceptions)
        else:
            for exception, path in all_exceptions:
                print(f'{path.relative_to(root)}: {exception}')
            return 1
        if list:
            print('failed to import:')
            for p in paths:
                print(p)
            return 1
    return 0


def mainargs(argv=None):
    pser = argparse.ArgumentParser()
    pser.add_argument('root', nargs='?', default=Path.cwd(), type=Path)
    pser.add_argument('-c', '--clear-cache', action='store_true')
    pser.add_argument('-l', '--list', action='store_true')
    pser.add_argument('--raise', action='store_true', dest='raise_', help='raise exceptions instead of printing them')
    args = pser.parse_args(argv)
    return vars(args)


def all_modules(root):
    dirs_with_inits = (p.parent for p in root.rglob('__init__.py'))
    modulepaths = collapse(dir.glob('*.py') for dir in dirs_with_inits)
    yield from ((path_to_module(path, root), path) for path in modulepaths)


def path_to_module(path, root):
    path = path.relative_to(root)
    return '.'.join((root.name, *path.parts[:-1]))


if __name__ == "__main__":
    sys.exit(main(**mainargs()))
