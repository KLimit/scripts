import itertools
import re
import shutil
import subprocess
import sys
import textwrap

WINGET = shutil.which('winget.exe')
SEARCH = 'search'
SHOW = 'show'
def _winget_subcmd(cmd):
    def sub(arg):
        return subprocess.run(
            [WINGET, cmd, arg],
            text=True,
            capture_output=True,
            encoding='utf-8',
        )
    return sub
_winget_search = _winget_subcmd(SEARCH)
_winget_show = _winget_subcmd(SHOW)


throbber = re.compile(r'^\s*[-\\|/]\s*$')
div = re.compile('-+')
junk = re.compile(
    r'''
    [-\\|/]  # throbber
    | -+  # dividing line
    | ^$  # empty line
    |.*[0-9.]+\s.B\s/\s[0-9.]+\s.B  # loading bar (not sure what char is used)
    |\s*[█▒]+\s+\d+%  # another loading bar
    ''',
    re.X,
)
def strip_noise(st):
    return '\n'.join(
        line
        for line in st.splitlines()
        if not junk.match(line.strip())
    )


def table_from_headers(st):
    """Make list of lists using first line of string as headers.

    Columns are based on position of headers.
    """
    header, *lines = st.splitlines()
    indices = header_positions(header)
    return [
        header.split(),
        *(splitat(line, *indices) for line in lines)
    ]


def dicts_from_table(tab):
    header, *rows = tab
    return [dict(zip(header, row)) for row in rows]


def header_positions(line):
    names = line.split()
    return [line.index(name) for name in names]


def splitat(st, *positions, strip=True):
    """Split a string at the given positions"""
    positions += (None, )
    slices = [
        slice(start, end-1 if end is not None else end)
        for start, end in itertools.pairwise(positions)
    ]
    strip = str.strip if strip else lambda x: x
    return [
        strip(st[slice])
        for slice in slices
    ]


nomatch = 'No package found matching input criteria.'

def search(prog):
    result = _winget_search(prog)
    if result.returncode:
        return
    table = table_from_headers(strip_noise(result.stdout))
    return table


def show(winget_id):
    result = _winget_show(winget_id)
    if result.returncode:
        return
    return parse_metadata(strip_noise(result.stdout), winget_id)


def pretty_metadata(md):
    indent = 0
    for key in ['Id', 'Moniker', 'Author', 'Homepage', 'License', 'Description']:
        data = md.get(key, '')
        if isinstance(data, str):
            data = [data]
        for line in data:
            for wrappedline in textwrap.wrap(line):
                print(textwrap.indent(wrappedline, ' '*indent))
        # indent after the first line (which we can guarantee is Id if from
        # parse_metadata)
        if not indent:
            indent = 2


def parse_metadata(st, winget_id):
    # WARN: This is not complete; it will fail when there are multiline keys
    # with a value on the same line as the key
    metadata = {'Id': winget_id}
    # /(.+?):/ use non-greedy .+? to stop at first colon
    kv = re.compile(r'^(\w.+?): ?(.*)')
    lines = list(reversed(st.splitlines()))
    while lines:
        line = lines.pop()
        if line.startswith('Found') and all(c in line for c in '[]'):
            continue
        k, v = kv.match(line).groups()
        k = k.strip()
        if not v:
            v = []
            while lines and not kv.match(line:=lines.pop()):
                v.append(line.strip())
            # put the next kv match back
            if lines:
                lines.append(line)
        if v:
            metadata[k] = v
    for key in ('Documentation', 'Installer'):
        for subitem in metadata.pop(key, []):
            k, _, v = subitem.partition(':')
            metadata[k.strip()] = v.strip()
    return metadata


def search_and_pick(prog):
    found = search(prog)
    if not found:
        print(f'nothing found for {prog}')
        return
    options = [r['Id'] for r in dicts_from_table(found)]
    if len(options) == 1:
        print(f'found "{options[0]}" for {prog}')
        return options[0]
    return pick(options, prog)


def pick(options, prog=''):
    options = {str(n): opt for n, opt in enumerate(options)}
    def listopts():
        for n, opt in options.items():
            print(f'{n}) {opt}')
    def getoption(choice):
        if choice in options:
            return options[choice]
        for opt in options.values():
            if choice.casefold() == opt.casefold():
                return opt
    commands = {
        'l': 'list',
        'i': 'info',
        's': 'skip',
        'h': 'help',
        '?': 'help',
    }
    prompt = f'pick an option (0-{len(options)-1}) or command ({",".join(commands.keys())})> '
    if prog:
        prompt = f'{prog}: ' + prompt
    listopts()
    while True:
        choice = input(prompt)
        if (chosen:=getoption(choice)) is not None:
            return chosen
        # if the input was a choice or the option itself (case insensitive)
        choice, *rest = choice
        choice = commands.get(choice, 'help')
        match choice:
            case 'list':
                listopts()
            case 'info':
                rest = ''.join(rest).strip()
                if rest == '*':
                    for prog in options.values():
                        pretty_metadata(show(prog))
                    continue
                opt = getoption(rest)
                if opt is None:
                    print(f'{rest} is not one of the options')
                else:
                    pretty_metadata(show(opt))
            case 'skip':
                return
            case 'help':
                print(', '.join(f'{k}={v}' for k, v in commands.items()))


def main(name, *argv):
    helpflags = ('-h', '--help', '-?', '/?')
    if not argv or any(h in map(str.casefold, argv) for h in helpflags):
        print(f'{name} query [query [query ...]]')
        print('Search the winget repository for each query and choose from any matches')
        print('Prints the ids of the chosen programs (or empty line, if skipped)')
        sys.exit()
    # TODO: get subsequent queries in background
    winget_ids = []
    for prog in argv:
        winget_ids.append(search_and_pick(prog))
    # TODO: option to install
    for i in winget_ids:
        print(line)


if __name__ == '__main__':
    main(*sys.argv)
