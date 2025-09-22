#!/usr/bin/env python3
import math
import operator
import sys

def rpncalc(commands, verbose=False):
    if verbose:
        p = print
    else:
        def p(*args, **nargs):
            ...
    stack = []
    for i, n in enumerate(commands):
        p(f'--{i}--')
        p(stack)
        op = None
        nargs = 2
        match n:
            case '+': op = operator.add
            case '-': op = operator.sub
            case '*': op = operator.mul
            case '/': op = operator.truediv
            case '%': op = operator.mod
            case '^':
                op = operator.pow
            case 'v':
                op = math.sqrt
                nargs = 1
            case 'p':
                try:
                    print(stack.pop())
                except IndexError:
                    pass
                continue
            case _:
                if (negative:=n.startswith('_')):
                    n = n[1:]
                n = float(n)
                if negative:
                    n *= -1
                stack.append(n)
        if op is not None:
            args = [stack.pop() for _ in range(nargs)]
            p(f'{n}{args}')
            stack.append(op(*reversed(args)))
        p(stack)
    return stack


if __name__ == '__main__':
    argv = [
        arg for arg in sys.argv
        if arg.lower() not in ('-v', '--verbose')
    ]
    if any(h in map(str.lower, argv) for h in ('-h', '--help')):
        from textwrap import dedent, indent
        with open(__file__) as f:
            lines = iter(f)
            while 'match' not in (line:=next(lines)):
                ...
            help = []
            while 'if op is not None:' not in (line:=next(lines)):
                help.append(line)
            print('dc.py [-v|--verbose] *commands | [-h|--help]', file=sys.stderr)
            print(
                indent(dedent(''.join(help)), '    '),
                file=sys.stderr,
            )
            print('(does not read stdin)', file=sys.stderr)
            sys.exit()
    rpncalc(argv[1:], verbose=len(argv)<len(sys.argv))
