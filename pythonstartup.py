#!/usr/bin/env python3
"""Miscellaneous niceties when running in inspect mode."""
from __future__ import (
    absolute_import,
    # division,
    print_function,
    unicode_literals,
)
import functools
import logging
import math
from pathlib import Path
import sys

try:
    from py_units import unitter, Quantity
except ImportError:
    print('could not import py_units', file=sys.stderr)

# Python 3 (and above?)
if sys.version_info.major != 2:
    from importlib import reload


def parallel(*rs):
    return 1/sum(1/r for r in rs)

def div(rtop, rbot, *, vs=1):
    return vs * rbot / (rtop + rbot)

def inv(x):
    return 1 / x

def filt(a, b):
    """Calculate the missing value for a first-order RC filter."""
    # f = 1 / (tau * r * c)
    # x = 1 / (tau * a * b)
    return 1/(math.tau * a * b)

def ed(prompt='> ', end='.', transform=None):
    """Minimal ed-like line editor. Stop with '.' on a single line."""
    lines = []
    if transform is None:
        transform = lambda _: _
    if not prompt.endswith('> '):
        prompt = prompt + '> '
    while (line:=input(prompt)) != end:
        lines.append(transform(line))
    return lines

def eager(fn=None, /, *, type=list):
    def wrapper(fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            return type(fn(*args, **kwargs))
        return wrapped
    if fn is None:
        return wrapper
    return wrapper(fn)

class ContextGroup:
    def __init__(self, *cms):
        self.cms = cms
    def __enter__(self):
        return tuple(cms.__enter__() for cms in self.cms)
    def __exit__(self, *args, **kwargs):
        return tuple(cms.__exit__(*args, **kwargs) for cms in self.cms)


def save(fname, *objects, append=True):
    import inspect
    mode = 'w'
    if append:
        mode = 'a'
    with open(fname, mode) as f:
        def p(*args, **kwargs):
            print(*args, **kwargs, file=f)
        for obj in objects:
            try:
                p(inspect.getsource(obj))
            except TypeError:
                try:
                    p(f'{obj} = {globals()[obj]!r}')
                except KeyError:
                    p(f'# {obj}')
                except TypeError:
                    import uuid
                    u = uuid.uuid4()
                    p(f'_{hex(u.fields[0])[2:]} = {obj!r}')

def tab(seq):
    seq = list(seq)
    n = 1
    col = os.get_terminal_size().columns
    maketable = lambda n: tabulate.tabulate(more_itertools.grouper(seq, n))
    while True:
        table = maketable(n)
        if len(table.splitlines()[0]) > col:
            break
        if n > len(seq):
            break
        n += 1
    return maketable(n-1)
