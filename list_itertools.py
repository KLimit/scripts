#!/usr/bin/env python3
"""Make the output of itertools functions into lists for ease of use."""
from functools import wraps
import itertools


def lister(fn):
    @wraps(fn)
    def listed(*args, **kwargs):
        return list(fn(*args, **kwargs))
    return listed


# bad way
tee = lister(itertools.tee)
accumulate = lister(itertools.accumulate)
dropwhile = lister(itertools.dropwhile)
takewhile = lister(itertools.takewhile)
islice = lister(itertools.islice)
starmap = lister(itertools.starmap)
chain = lister(itertools.chain)
compress = lister(itertools.compress)
filterfalse = lister(itertools.filterfalse)
zip_longest = lister(itertools.zip_longest)
pairwise = lister(itertools.pairwise)
@wraps(itertools.groupby)
def groupby(*args, **kwargs):
    grouped = itertools.groupby(*args, **kwargs)
    return [(name, list(grouper)) for name, grouper in grouped]
# infinite
count = itertools.count
cycle = itertools.cycle
repeat = itertools.repeat
# returns tuples
product = itertools.product
permutations = itertools.permutations
combinations = itertools.combinations
combinations_with_replacement = itertools.combinations_with_replacement
