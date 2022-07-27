"""Incredibly basic TUI for viewing a single monitor item."""

import argparse

from motiv_python_utils.device_interface.can.frontend import canterminal


CLEAR = '\033[2J\033[H'


def main(node, monitor, binkeys):
    """Loop and continuously print the monitor."""
    term = canterminal.DiagCanTerminal()
    term.preloop()
    term.active_node = node
    while True:
        mon = dict(term._get_monitor(monitor))
        mon.update({
            key: bin(item) for key, item in mon.items() if key in binkeys
        })
        mon = stronemonitor(mon)
        print(CLEAR)
        print(mon)
    term.postloop()


def stronemonitor(mon):
    """Print one monitor with string formatting."""
    keywidth = max(len(key) for key in mon)
    monstr = [
        '{k:{w}}: {i}'.format(k=key, i=item, w=keywidth)
        for key, item in mon.items()
    ]
    return '\n'.join(monstr)


def _args(argv=None):
    """Process argument lists into kwarg dict for main()."""
    pser = argparse.ArgumentParser()
    pser.add_argument('node', type=int)
    pser.add_argument('monitor')
    pser.add_argument('binkeys', nargs='*')
    args = pser.parse_args(argv)
    return vars(args)


if __name__ == '__main__':
    main(**_args())
