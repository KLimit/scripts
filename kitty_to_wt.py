#!/usr/bin/env python3
import argparse
import json
import sys

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


def main(inp, name):
    inp = (line.strip().split() for line in inp)
    colorscheme = {'name': name}
    colorscheme.update((keymap[name], color) for name, color in inp)
    colorscheme['name'] = name
    print(json.dumps(colorscheme))


def mainargs(argv=None):
    pser = argparse.ArgumentParser()
    pser.add_argument('name')
    pser.add_argument('inp', type=argparse.FileType('r'), default='-')
    args = pser.parse_args(argv)
    return vars(args)



if __name__ == "__main__":
    sys.exit(main(**mainargs()))
