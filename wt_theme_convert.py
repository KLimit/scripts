#!/usr/bin/env python3
import argparse
import enum
from functools import partial
import json
import sys
import tomllib



def kitty(inp, name):
    keymap = {
        "background": "background",
        "foreground": "foreground",
        "cursor": "cursorColor",
        "color0": "black",
        "color1": "red",
        "color2": "green",
        "color3": "yellow",
        "color4": "blue",
        "color5": "purple",
        "color6": "cyan",
        "color7": "white",
        "color8": "brightBlack",
        "color9": "brightRed",
        "color10": "brightGreen",
        "color11": "brightYellow",
        "color12": "brightBlue",
        "color13": "brightPurple",
        "color14": "brightCyan",
        "color15": "brightWhite",
        "selection_background": "selectionBackground",
        "selection_foreground": "selectionForeground",
    }
    inp = (line.strip().split() for line in inp)
    scheme = {'name': name}
    scheme.update((keymap[name], color) for name, color in inp)
    scheme['name'] = name
    return scheme


def alacritty(inp, name):
    inp = inp.read()
    inp = tomllib.loads(inp)['colors']
    # alacritty uses magenta instead of purple
    for d in (inp['normal'], inp['bright']):
        d['purple'] = d.pop('magenta')
    scheme = {'name': name}
    for d in (
        inp['primary'],  # fg, bg
        inp['normal'],
        {camel('bright', name): color for name, color in inp['bright'].items()},
        # additional colors
        {
            'selectionBackground': inp['selection']['background'],
            'cursorColor': inp['cursor']['cursor']
        },
    ):
        scheme.update(d)
    return scheme


def camel(prefix, suffix):
    return prefix + suffix.capitalize()


def main(input_type, inp, name):
    match input_type:
        case Types.KITTY:
            converter = kitty
        case Types.ALACRITTY:
            converter = alacritty
    print(json.dumps(converter(inp, name)))


class Types(enum.StrEnum):
    KITTY = enum.auto()
    ALACRITTY = enum.auto()


def mainargs(argv=None):
    pser = argparse.ArgumentParser()
    pser.add_argument('input_type', choices=list(Types))
    pser.add_argument('name')
    pser.add_argument('inp', type=argparse.FileType('r'), default='-')
    args = pser.parse_args(argv)
    return vars(args)



if __name__ == "__main__":
    sys.exit(main(**mainargs()))
