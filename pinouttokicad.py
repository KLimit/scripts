#! /usr/bin/python3
"""Take a kicad_sym file and a pinout json and change the pin names."""

import argparse
import fileinput
from itertools import groupby
import io
import json
import re
import shutil
import sys


def main():
    """Define the script here to avoid upsetting linters w bad variable names."""
    parser = argparse.ArgumentParser()
    parser.add_argument('pinout', type=argparse.FileType('r'))
    parser.add_argument('connector', type=str)
    parser.add_argument('libfile', type=argparse.FileType('r'), default=sys.stdin)
    outfile = parser.add_mutually_exclusive_group()
    outfile.add_argument('-o', '--outfile', type=argparse.FileType('w'), default=sys.stdout)
    outfile.add_argument('-i', '--in-place', action='store_true')
    args = parser.parse_args()
    pinout = json.load(args.pinout)
    args.pinout.close()
    pinout = {
        connector: list(pins)
        for connector, pins in groupby(pinout, lambda x: x['connector'])
    }
    pins = pinout[args.connector]
    pins = {pin['pin']: pin['name'] for pin in pins}
    if args.in_place:
        raise Exception('In-place writing is not supported at this time.')
        args.outfile = io.StringIO()
    connectorpttn = re.compile(r'(?<=\(name ")Pin_(\d+)')
    for line in args.libfile:
        subfn = lambda m: pins[m.group(1)]
        line = connectorpttn.sub(subfn, line)
        print(line, file=args.outfile, end='')
    args.libfile.close()
    if args.in_place:
        args.libfile = open(args.libfile.name, 'w')
        args.outfile.seek(0)
        shutil.copyfileobj(args.outfile, args.libfile)
        args.libfile.close()
        args.outfile.close()


if __name__ == '__main__':
    main()
