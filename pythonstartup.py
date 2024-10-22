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
from pathlib import Path
import sys

try:
    from py_units import unitter, Quantity
except Importerror:
    print('could not import py_units', file=sys.stderr)

# Python 3 (and above?)
if sys.version_info.major != 2:
    from importlib import reload


def parallel(*rs):
    return 1/sum(1/r for r in rs)


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
