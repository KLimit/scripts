#!/usr/bin/env python3

def grid(*columns, aligns=None, delim=',', default_align='r'):
    if not columns:
        return ''
    widths = [max(map(len, col)) for col in columns]
    align = {'l': str.ljust, 'r': str.rjust, 'c': str.center}
    # TODO: modularize this and add similar feature for fill similar to aligns
    if aligns is None:
        aligns = default_align
    if isinstance(aligns, str):
        aligns = aligns.lower()
        if len(aligns) == 1:
            default_align = aligns
        while len(aligns) < len(columns):
            aligns += default_align
    if isinstance(aligns, dict):
        aligns = [aligns.get(n, default_align) for n in range(len(columns))]
    return [
        delim.join(
            align[aligns[n]](item, width)
            for n, (width, item) in enumerate(zip(widths, row))
        ).rstrip()
        for row in zip(*columns)
    ]

