#!/usr/bin/env python3
import argparse
import sys
pser = argparse.ArgumentParser()
pser.add_argument('title', nargs='?')
pser.add_argument('query', nargs='?')
args = pser.parse_args()
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
