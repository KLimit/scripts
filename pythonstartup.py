#!/usr/bin/env python3
"""Miscellaneous niceties when running in inspect mode."""
from __future__ import (
    absolute_import,
    # division,
    print_function,
    unicode_literals,
)
import logging
from pathlib import Path
import sys


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
