"""Store the last name and prepend it when necessary.

I relented and am doing this in Python instead of Perl.
"""

import fileinput
import re


def main():
    """Invoke from cli."""
    numpttn = r'_?\d*$'
    prevname = ''
    for line in fileinput.input():
        line = line.strip()
        if re.match(numpttn, line):
            # only here if the line is just the number
            line = prevname + line
        print(line)
        currentname = re.sub(numpttn, '', line)
        if currentname != prevname:
            prevname = currentname


if __name__ == '__main__':
    main()
