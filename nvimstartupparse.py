#!/usr/bin/env python3
"""quick and dirty `n?vim --startuptime <output>` parser."""
import argparse
import csv
import re
import sys


def tryfloat(str_):
    try:
        str_ = str_.strip(":")
    except AttributeError:
        pass
    try:
        return float(str_)
    except ValueError:
        return str_


class ProfileChunk:
    def __init__(self, clock, selfsourced, self_, step):
        self.clock = clock
        self.selfsourced = selfsourced
        self.self_ = self_
        self.step = self.parsestep(step)

    def parsestep(self, step):
        if "sourcing" in step:
            step = step.split()[-1]
            step = step.split("\\")[-1]
        else:
            step = step.split("'")[1]
        return step

    def __repr__(self):
        return repr(list(self))

    def __iter__(self):
        for attr in (self.clock, self.selfsourced, self.self_, self.step):
            yield attr


if __name__ == '__main__':
    pser = argparse.ArgumentParser()
    pser.add_argument('logfile')
    pser.add_argument('--ascending', action='store_true', help='sort fast -> slow')
    args = pser.parse_args()

    with open(args.logfile) as f:
        startups = f.read()
    startups = [line.strip() for line in startups.split('\n')]

    srcreq = re.compile('sourcing|require')
    startups = [
        line.split(maxsplit=3) for line in startups
        if srcreq.search(line)
        and not re.search('sourcing vimrc file', line)
        and not re.search('Program Files', line)
    ]
    # startups = [line for line in startups if srcreq.search(line)]
    # startups = [line for line in startups if not re.search('sourcing vimrc file', line)]
    # startups = [line for line in startups if not re.search("Program Files", line)]
    # startups = [line.split(maxsplit=3) for line in startups]
    startups = [tuple(tryfloat(item) for item in line) for line in startups]
    startups = [ProfileChunk(*line) for line in startups]
    selfsourced = sorted(startups, key=lambda chunk: chunk.selfsourced)
    if not args.ascending:
        selfsourced = reversed(selfsourced)
    writer = csv.writer(sys.stdout)
    writer.writerow('clock self+sourced self name'.split())
    writer.writerows(iter(chunk) for chunk in selfsourced)
