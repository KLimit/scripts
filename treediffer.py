#!/usr/bin/env python3
import argparse
import csv
import hashlib
from pathlib import Path
import sys


def main(path_a, path_b, recurse, thorough, hash, csv):
    path_a, path_b = Path(path_a), Path(path_b)
    a, b = get_tree(path_a, recurse), get_tree(path_b, recurse)
    a_only, b_only = a - b, b - a
    both = a & b
    diff = [
        path
        for path in both
        if different(path_a/path, path_b/path, thorough, hashfunc=hash)
    ]
    if csv:
        diff = [
            path
            for path in diff
            if (csv_differ(path_a/path, path_b/path) if path.suffix.casefold() == '.csv' else True)
        ]
    diff.sort()
    print(f'a: {path_a} != b: {path_b}')
    for file in a_only:
        print(f'{"a"/file} not in b')
    for file in b_only:
        print(f'{"b"/file} not in a')
    for file in diff:
        print(f'{file} differs')
    return 0


def get_tree(root, recurse):
    globber = Path.rglob if recurse else Path.glob
    return {node.relative_to(root) for node in globber(root, '*')}


def different(path_a, path_b, thorough=True, chunksize=1024, hashfunc='sha256'):
    # if one is a directory and one is a file, they must be different
    if path_a.is_file() != path_b.is_file():
        return True
    # if both are directories, they are the same?
    if path_a.is_dir() and path_b.is_dir():
        return False
    # if they are different sizes, they must be different
    if path_a.stat().st_size != path_b.stat().st_size:
        return True
    digest = lambda file: hashlib.file_digest(file, hashfunc).digest()
    with open(path_a, 'rb') as file_a, open(path_b, 'rb') as file_b:
        # files will be different if hashes are different
        if digest(file_a) != digest(file_b):
            return True
    # last resort is to compare bytes
    if thorough:
        return contents_differ(path_a, path_b, chunksize)
    return False


def chunker(stream, chunksize):
    while chunk := stream.read(chunksize):
        yield chunk
    yield chunk

def contents_differ(file_a, file_b, chunksize):
    with open(file_a, 'rb') as file_a, open(file_b, 'rb') as file_b:
        return any(
            chunk_a != chunk_b
            for chunk_a, chunk_b
            in zip(chunker(file_a, chunksize), chunker(file_b, chunksize))
        )

def csv_differ(csv_a, csv_b):
    with open(csv_a, newline='') as a, open(csv_b, newline='') as b:
        a = csv.reader(a)
        b = csv.reader(b)
        toreturn = list(
            normalize_row(row_a) != normalize_row(row_b)
            for row_a, row_b
            in zip(a, b)
        )
    # if 'P101' in str(csv_a) and 'Circuit Summari' in str(csv_a):
    #     breakpoint()
    return any(toreturn)


def normalize_row(row):
    newrow = []
    for item in row:
        try:
            item = float(item)
            if item.is_integer():
                newrow.append(int(item))
            else:
                newrow.append(item)
        except ValueError:
            newrow.append(item)
    return newrow

def mainargs(argv=None):
    pser = argparse.ArgumentParser()
    pser.add_argument('path_a')
    pser.add_argument('path_b')
    pser.add_argument('--no-recurse', dest='recurse', action='store_false')
    pser.add_argument('--fast', dest='thorough', action='store_false', help="don't compare contents if hashes match")
    pser.add_argument('--hash', default='sha256', choices=hashlib.algorithms_available)
    pser.add_argument('--csv', action='store_true', help='compare csv files semantically')
    args = pser.parse_args(argv)
    return vars(args)


if __name__ == "__main__":
    sys.exit(main(**mainargs()))
