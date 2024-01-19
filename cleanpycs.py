#/usr/bin/python3
"""Clean any existing *.pyc files that don't have a corresponding .py file."""

import argparse
from cmd import Cmd
from functools import partial
from pathlib import Path


def args(argv=None):
    """Process args for main."""
    pser = argparse.ArgumentParser()
    pser.add_argument('-c', '--confirm', action='store_true')
    pser.add_argument('-v', '--verbose', action='store_true')
    pser.add_argument('-n', '--what-if', action='store_true')
    pser.add_argument('startdir', type=Path, default=Path(), nargs='?')
    return vars(pser.parse_args(argv))


def main(startdir, confirm, verbose, what_if):
    """Glob for all *.pyc and *.py files; delete the orphan .pyc files.

    startdir: starting directory
    confirm: ask user before deleting
    what_if: do not delete
    """
    pys = [py.stem for py in startdir.rglob('*.py')]
    pycs = list(startdir.rglob('*.pyc'))
    orphans = [pyc for pyc in pycs if pyc.stem not in pys]
    # return pys, pycs, orphans
    def conf(prompt):
        if not confirm:
            return True
        return _confirm(('y', 'n'), prompt, def_choice=True)
    for orphan in orphans:
        if verbose or what_if:
            print(orphan)
        if not what_if and conf(f'Delete {orphan}?'):
            orphan.unlink()


def _confirm(truefalse, prompt, def_choice=None):
    prompt_start = prompt.strip()
    class Confirmer(Cmd):
        default_choice = None if def_choice is None else bool(def_choice)
        result = default_choice
        true, false = truefalse
        ptrue, pfalse = (state.lower() for state in truefalse)
        if default_choice is not None:
            ptrue = ptrue.capitalize() if default_choice else ptrue
            pfalse = pfalse if default_choice else pfalse.capitalize()
        prompt = prompt_start + f' [{ptrue}/{pfalse}] '
        bad = f'"{{}}" is not an option. Choose from {ptrue} and {pfalse}.'
        def precmd(self, line):
            return line.casefold().strip()
        def default(self, line):
            if line not in (self.true, self.false):
                print(bad.format(line))
                return
            self.result = line == self.true
            return True
        def emptyline(self):
            if self.default_choice is not None:
                return True
    confirmer = Confirmer()
    confirmer.cmdloop()
    return confirmer.result


if __name__ == '__main__':
    main(**args())
