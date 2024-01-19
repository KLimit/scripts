#!/usr/bin/env python3
import argparse
import sys
pser = argparse.ArgumentParser()
pser.add_argument('title', nargs='?')
pser.add_argument('query', nargs='?')
pser.add_argument('-y', '--yes', action='store_true', help='return w/ exit code 0')
pser.add_argument('-n', '--no', action='store_true', help='return w/ nonzero exit code (overrides --yes)')
args = pser.parse_args()
if args.no:
    sys.exit(2)
elif args.yes:
    sys.exit(0)
title = f'{args.title}:' if args.title else ''
query = f' {args.query} ' if args.query else ''
options = 'yN'
prompt = f'{title}{query}({options}) > '
# input_ = input
# def input(prompt):
#     print(prompt, end='', flush=True)
#     input_()
while (selection := input(prompt).casefold()) not in options.casefold():
    pass
if selection == 'y':
    sys.exit(0)
sys.exit(1)
