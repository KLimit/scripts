#!/usr/bin/env python3
import os
def ruler(end=-1, interval=10, offset=0, tick='|', line='.'):
    if len(tick) > 1 or len(line) > 1:
        raise ValueError('ticks and line markers must be one character long')
    if end < 0:
        end = os.get_terminal_size().columns
    end = end - offset
    nticks = end % interval
    segment = f'{tick}{{n:{line}<{interval-1}}}'
    ruler_ = ''.join(
        segment.format(n=n)
        for n in [1, *range(interval, end, interval)]
    )
    # TODO: add final marker if there's enough room, but not enough for a whole
    # segment
    # if end - len(ruler_)
    return ruler_

def main(argv=None):
    import argparse
    pser = argparse.ArgumentParser()
    pser.add_argument('-n', '--end', default=-1, type=int)
    pser.add_argument('-i', '--interval', default=10, type=int)
    pser.add_argument('-o', '--offset', default=0, type=int)
    pser.add_argument('-t', '--tick', default='|')
    pser.add_argument('-l', '--line', default='.')
    args = pser.parse_args(argv)
    print(ruler(**vars(args)))

if __name__ == '__main__':
    # TODO: add command line interface
    main()
