"""Compare the items in two order-independent sets."""
from pathlib import Path

from clify import clify


def unique(l):
    return len(l) == len(set(l))



def diff(a, b, key=None):
    a, b = set(a), set(b)
    same = a & b
    aonly = a - b
    bonly = b - a
    for item in sorted(same, key=key):
        yield item, item
    for item in sorted(aonly, key=key):
        yield item, None
    for item in sorted(bonly, key=key):
        yield None, item


@clify
def main(a:Path, b: Path):
    a = a.read_text().splitlines()
    b = b.read_text().splitlines()
    d = list(diff(a, b))
    longa, longb = [max(len(s) for s in sub if s) for sub in zip(*d)]
    symbol = '='
    for a, b in d:
        if b is None:
            symbol = '-'
            b = ''
        elif a is None:
            symbol = '+'
            a = ''
        print(f'({symbol}) {a:>{longa}} -> {b:>{longb}}')
