#!/usr/bin/env python3
"""Use a shlexer to try to ~smartly filter out line noise and just get numbers

Mainly expecting xml-type stuff (see ABC precharge data).
TODO:
    - Get the grouper recipe from itertools
    - Do a sanity check of something like bool(len(data) % len(headers))
    - Use csv dictwriter to make the output
    - Need to figure out what to do with index columns

Index column plan: don't look for them. Only count things with an equals sign
as tokens. Shlex once instead of twice like it's currently set up to do and
split on equals sign.
Downside to this is that it's less flexible. Upside is that it's easier.
Could make a base case that any number prepended by an underscore is an index,
but that might be too rigid as well.
Maybe any number without an equals sign.
"""
import csv
import fileinput
import shlex


data = '0123456789.'
alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
dataords = {key: None for key in (ord(f'{num}') for num in data)}


def main(inp=None):
    """Get input, shlex it."""
    rawdata = [line.strip() for line in fileinput.input(inp)]
    rawdata = '\n'.join(rawdata)
    data = shlexdata(rawdata)


def shlexdata(inpstr):
    """Extract numerical data"""
    # set posix to remove quoted characters
    datashlex = shlex.shlex(instream=inpstr, posix=True)
    datashlex.wordchars = '.0123456789'
    datashlex.whitespace += '<>/_=' + alpha
    tokens = [datashlex.get_token()]
    while all(tokens):
        tokens.append(datashlex.get_token())
    # only breaks after one token is Falsy
    tokens.pop()
    return tokens


def headers(inpstr):
    """Extract numerical data"""
    # set posix to remove quoted characters
    datashlex = shlex.shlex(instream=inpstr, posix=True)
    datashlex.wordchars = datashlex.wordchars.translate(dataords)
    datashlex.whitespace += '<>/="' + data
    tokens = [datashlex.get_token()]
    while all(tokens):
        tokens.append(datashlex.get_token())
    # only breaks after one token is Falsy
    tokens.pop()
    tokens = _uniq(tokens)
    return tokens


def _uniq(iterable):
    """Get unique items and preserve order."""
    seen = []
    for item in iterable[:]:
        if item in seen:
            iterable.remove(item)
        seen.append(item)
    return iterable


if __name__ == '__main__':
    main()
