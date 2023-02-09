#!/usr/bin/env python3
"""Kanata and Komorebi window manager."""

import atexit
from functools import partial
from pathlib import Path
from shutil import which
from subprocess import Popen, run


def main():
    """Run a series of commands."""
    kanata = which('kanata')
    kanataconf = Path('~/.config/kanata.kbd').expanduser()
    kanata_proc = Popen(f'{kanata} --cfg {kanataconf}')
    komorebi = which('komorebi')
    # done with komorebi for now
    komorebi_proc = Popen(f'{komorebi} --await-configuration')
    komorebic = which('komorebic')
    komoconf = Path('~/.config/komorebi/komorebirc').expanduser()
    with open(komoconf) as k:
        komoconf = k.readlines()
    sent_complete = False
    for conf in komoconf:
        conf = conf.strip()
        sent_complete = 'complete-configuration' in conf
        run(f'{komorebic} {conf}')
    if not sent_complete:
        run(f'{komorebic} complete-configuration')
    atexit.register(partial(run, f'{komorebic} stop'))


if __name__ == '__main__':
    main()
