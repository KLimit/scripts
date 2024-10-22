import getpass
import importlib
import re
import sys

import psutil

get_confirmation = importlib.import_module('get-confirmation')


def search(pattern, smartcase=True):
    sensitive = not smartcase or any(c.isupper() for c in pattern)
    sensitive = not sensitive and re.IGNORECASE
    pattern = re.compile(pattern, sensitive)
    return [p for p in psutil.process_iter(['name']) if pattern.search(p.info['name'])]
def tree(iterable, key=None, level=0, char='-', indent=1, highlightchar='*', tohighlight=None):
    if key is None:
        def key(item):
            if isinstance(item, str):
                # usually pretty sane not to iterate over strings
                return []
            try:
                iter(item)
            except TypeError:
                return []
            return item
    tohighlight = tohighlight or []
    for item in iterable:
        bullet = highlightchar if item in tohighlight else char
        print(' '*indent*level + bullet + ' ' + str(item))
        sub = key(item)
        if sub:
            tree(sub, key, level+1, char, indent, highlightchar, tohighlight)
NEST_DONE = object()
def nest(iterable):
    iterable = iter(iterable)
    try:
        current = next(iterable)
        remaining = nest(iterable)
        return [current] + ([remaining] if remaining is not NEST_DONE else [])
    except StopIteration:
       return NEST_DONE


def yesno(question):
    options = 'yN'
    yes = 'y'.casefold()
    prompt = f'{question} ({options}) > '
    while (answer:= input(prompt)).casefold() not in 'yn':
        pass
    return answer == yes


def main(pattern):
    matches = search(pattern)
    if not matches:
        print(f'no processes match {pattern!r}', file=sys.stderr)
        sys.exit(1)
    only1 = len(matches) == 1
    for n, match in enumerate(matches, 1):
        tree([match.parent()])
        tree(
            [match],
            key=lambda p_: p_.children(),
            level=1,
            highlightchar=str(n) if not only1 else '*',
            tohighlight=[match],
        )
    if only1 and yesno('kill the process?'):
        matches[0].kill()
        sys.exit(0)
    else:
        try:
            while (answer:=int(input('which process to kill? > '))-1) not in range(len(matches)):
                pass
        except ValueError:
            answer = None
        if answer is not None:
            matches[answer].kill()
        else:
            sys.exit(2)
    sys.exit(0)

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError:
        print(f'usage: {__file__} pattern')
