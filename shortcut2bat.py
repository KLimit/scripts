#!/usr/bin/env python3
"""Convert a Windows .lnk shortcut to an equivalent batch file."""

import argparse
from pathlib import Path
import re
from shutil import which
from subprocess import run


pser = argparse.ArgumentParser()
pser.add_argument('--echo', action='store_true')
pser.add_argument(
    '--make-python-explicit',
    action='store_true',
    help='This is for shortcuts that invoke a python script, but do so by trusting that Windows is set up to run `.py` extensions with a Python interpreter. When enabled, replace this by explicitly running Python.'
)
pser.add_argument('shortcut')
args = pser.parse_args()

# some prog I have that can parse shortcuts
scut = which('scut')

def composebat(echo, make_python_explicit, working_dir, arguments, target, **kwargs):
    """Make the batch file.

    looks like this:

    {'Arguments': '/k "APC_IO.py & pause"',
     'Description': '',
     'Hotkey': '0',
     'Icon Index': '0',
     'Icon Path': '',
     'Show state': '1',
     'Target': 'C:/Windows/System32/cmd.exe',
     'Working Dir': 'C:/Beanstalk/Software/Code/Automated Test Setups/Under '
                    'Development'}
    """
    call = f'{target} {arguments}'
    if make_python_explicit:
        pyscript = re.search(r'\w*\.py', arguments, re.I).group()
        pause = ' & pause' if 'pause' in arguments else ''
        call = f'python {pyscript}{pause}'
    lines = [
        '@echo off' if not args.echo else '',
        f'cd {working_dir}',
        call,
    ]
    return '\n'.join(lines)


scutout = run([scut, '-dump', args.shortcut], capture_output=True, text=True)
scutout = scutout.stdout.strip()
# has the pattern /key:\s*item/
scutout = scutout.split('\n')
scutout = [line.split(':', maxsplit=1) for line in scutout]
scutout = {key.strip().lower().replace(' ', '_'): value.strip() for key, value in scutout}
bat = composebat(**(vars(args) | scutout))
print(bat)
