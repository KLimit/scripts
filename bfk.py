from collections import defaultdict
from itertools import dropwhile
import sys
def cleaninstructions(str):
    chars = tuple('><+-.[]')
    return ''.join(c for c in str if c in chars)
def main(instructions):
    data = defaultdict(int)
    pdata = 0
    pinstr = 0
    instructions = cleaninstructions(instructions)
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
        pinstr += 1

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
    main(' '.join(sys.argv[1:]))
