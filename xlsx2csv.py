#!/usr/bin/env python3
import collections
from contextlib import nullcontext
import csv
import itertools
import sys

import clify

import sxl


def sliding_window(iterable, n):
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


@clify.clify
def main(filename, sheet=1, outfile=None, rows:int=None, filtersize=3):
    try:
        sheet = int(sheet)
    except ValueError:
        pass
    wb = sxl.Workbook(filename)
    ws = wb.sheets[sheet]
    if outfile is None:
        outcontext = nullcontext(sys.stdout)
    else:
        outcontext = open(outfile, 'w', newline='')
    if rows is not None:
        rows += 1
    with outcontext as f:
        writer = csv.writer(f)
        for row in trimmed(ws.rows[slice(1, rows)], filtersize):
            writer.writerow(row)


def trimmed(rows, filtersize, trim_columns=True):
    rows = itertools.chain(rows, itertools.repeat([None]))
    firstrow = next(rows)
    lastcolumn = None
    if trim_columns:
        lastcolumn = 0
        for cell in reversed(firstrow):
            if cell is not None:
                break
            lastcolumn -= 1
    colslice = slice(None, lastcolumn)
    yield firstrow[colslice]
    for window in sliding_window(rows, filtersize):
        if all(all_none(row) for row in window):
            break
        yield window[0][colslice]


def all_none(seq):
    return all(x is None for x in seq)
