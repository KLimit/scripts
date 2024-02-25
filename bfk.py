import argparse
from collections import defaultdict
import sys
import time


class Memory(dict):
    bits = 8
    def __getitem__(self, key):
        if key not in self:
            self[key] = 0
        return super().__getitem__(key)
    def __setitem__(self, key, value):
        super().__setitem__(key, value % 2**self.bits)


def main(instructions, verbose=False):
    data = Memory()
    pdata = 0
    pinstr = 0
    instructions = ''.join(c for c in instructions if c in '<>+-.,[]')
    if verbose:
        print(instructions, file=sys.stderr)
    while pinstr < len(instructions):
        instruction = instructions[pinstr]
        match instruction:
            case '>':
                pdata += 1
            case '<':
                pdata -= 1
            case '+':
                data[pdata] += 1
            case '-':
                data[pdata] -= 1
            case '.':
                print(chr(data[pdata]), end='')
            case ',':
                data[pdata] = ord(input())
            case '[':  # ] (to appease the indenter)
                if not data[pdata]:
                    pinstr = findmatch(pinstr, instructions)
            case ']':
                if data[pdata]:
                    # jump back
                    pinstr = findmatch(pinstr, instructions)
        if verbose:
            print('\r', file=sys.stderr, end='')
            print(' '*len(instructions), file=sys.stderr, end='')
            print('\r', file=sys.stderr, end='')
            print(' '*pinstr+'^', file=sys.stderr, end='')
        pinstr += 1
    sys.stdout.flush()

def findmatch(position, instructions):
    startbracket = instructions[position]
    if startbracket not in '[]':
        raise ValueError('not at a branch point')
    indexed = enumerate(instructions)
    mate = ']'
    if startbracket == ']':
        mate = '['  # ]
        indexed = reversed(list(indexed))
        position = len(instructions) - position - 1
    indexed = list(indexed)[position:]  # only looking forward or backward
    brackets = [(i, b) for i, b in indexed if b in '[]']
    innercount = 0
    for index, bracket in brackets:
        if bracket == startbracket:
            innercount += 1
        else:
            innercount -= 1
        if not innercount:
            return index

if __name__ == "__main__":
    pser = argparse.ArgumentParser()
    pser.add_argument('-v', '--verbose', action='store_true')
    pser.add_argument('instructions', nargs='+')
    args = pser.parse_args()
    main(''.join(args.instructions), verbose=args.verbose)
