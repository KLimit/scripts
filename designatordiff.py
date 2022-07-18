"""Get the difference between two designator sets from a PCBA BOM."""


import argparse
import csv
import difflib
import os
import re


def load(filename):
    _, ext = os.path.splitext(filename)
    data = None
    if re.search('xl|od', ext):
        from pandas import read_excel
        import io
        data = read_excel(filename)
        data = io.StringIO(data.to_csv(index=False))
    with open(filename) if data is None else data as mycsv:
        reader = csv.DictReader(mycsv)
        return list(reader)


def _getcolumn(data, column):
    """Get items from column in data, separating by commas on the way."""
    sep = re.compile(', ?')
    return [split for item in data for split in sep.split(item[column])]


def diff(old, new, columns):
    """Compare the columns of old and new.

    old: filename of original
    new: filename of new
    columns: list containing one or two columns; if two, second item is for new
    """
    old, new = load(old), load(new)
    if len(columns) == 1:
        columns = columns*2
    old, new = _getcolumn(old, columns[0]), _getcolumn(new, columns[1])
    old, new = sorted(old), sorted(new)
    _diff = difflib.unified_diff(old, new, n=1, lineterm='')
    for line in _diff:
        print(line)


def main(argv=None):
    """Calculate and print the diff."""
    pser = argparse.ArgumentParser(description=__doc__)
    pser.add_argument('old', help='original file')
    pser.add_argument('new', help='new file')
    pser.add_argument(
        'columns',
        nargs='+',
        help='Key for columns to compare. Can give only one to use for both.'
    )
    args = pser.parse_args(argv)
    if len(args.columns > 2):
        raise IndexError('You can only specify two keys maximum.')
    diff(**vars(args))
