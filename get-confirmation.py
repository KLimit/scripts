#!/usr/bin/env python3
import argparse
import sys

def get_confirmation(title, query, options='yN', prompt=' '):
    # prompt = ' '.join([title, query, f'({options})', prompt])
    fullprompt = f'{title}: ' if title else ''
    if query:
        fullprompt += 'query '
    if options:
        fullprompt += f'({options})'
    prompt = fullprompt + prompt
    while (selection := input(prompt).casefold()) not in options.casefold():
        pass
    return selection == 'y'

if __name__ == '__main__':
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
    if get_confirmation(args.title, args.query):
        sys.exit(0)
    sys.exit(1)
