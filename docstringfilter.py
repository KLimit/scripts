"""Filter out everything but function/class definitions and docstrings.

henry.limm@motivps.com
"""

import fileinput
import re


def main():
    """Look for definitions and docstrings using a state machine."""
    starter = r'\s*(class|def)'
    docstring = '["\']{3}'
    indefinition = False
    indocstring = False
    for line in fileinput.input():
        line = line.strip()
        if re.match(starter, line):
            print(line)
            indefinition = True
        elif indefinition and re.search(docstring, line):
            print(line)
            indefinition = False
            indocstring = len(re.findall(docstring, line)) == 1
        elif indocstring:
            print(line)
            if re.search(docstring, line):
                indocstring = False
                print('')
        else:
            indefinition = False


if __name__ == '__main__':
    main()
