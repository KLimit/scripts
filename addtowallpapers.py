#!/usr/bin/env python3
import argparse
from collections import namedtuple
from dataclasses import dataclass
import os
from pathlib import Path
import re
import sys

import magic


DIMENSION = re.compile(r'(?<!density )(?P<width>\d+)\s*x\s*(?P<height>\d+)')
Dimension = namedtuple('Dimension', 'width height')


def get_dimensions(file_description):
    global DIMENSION
    match = DIMENSION.search(file_description)
    return Dimension(*map(int, match.groups()))


def aspect_ratio(width, height):
    return width/height


def is_image(file_description):
    # CONSIDER: make regex (depending on how libmagic works)
    return 'image'.casefold() in file_description.casefold()


def link_file(filename, target_dir, force=False):
    src = Path(filename).absolute()
    target = Path(target_dir) / src.name
    if not target.exists() or force:
        os.symlink(src, target)


@dataclass
class WallpaperWatcher:
    wallpaper_folder: str
    min_aspect: int = 1
    max_aspect: int = 999
    dry_run: bool = False
    verbose: bool = False
    recurse: bool = False
    force: bool = False
    def __post_init__(self):
        self.wallpaper_folder = Path(self.wallpaper_folder).absolute()

    @property
    def glob(self):
        return Path.rglob if self.recurse else Path.glob

    def make_link_name(self, filename):
        src = Path(filename).absolute()
        target = self.wallpaper_folder / src.name
        return target

    def run(self, path):
        file = Path(file).absolute()
        files = [file]
        if file.is_dir():
            files = [
                path for path in self.glob(file, '*')
                if path.is_file()
                and not path.is_relative_to(self.wallpaper_folder)
            ]



def main(
    file,
    wallpaper_folder,
    min_aspect=1,
    max_aspect=999,
    dry_run=False,
    verbose=False,
    recurse=False,
    force=False,
):
    file = Path(file).absolute()
    wallpaper_folder = Path(wallpaper_folder).absolute()
    if file.is_dir():
        globber = file.rglob if recurse else file.glob
        files = [
            path
            for path in globber('*')
            if path.is_file()
            and not path.is_relative_to(wallpaper_folder)
        ]
    else:
        files = [file]
    for file in files:
        description = magic.from_file(str(file))
        if not is_image(description):
            continue
        aspect = aspect_ratio(*get_dimensions(description))
        if min_aspect < aspect < max_aspect:
            # if (not target.exists() or force) and not dry_run:
            if not dry_run:
                link_file(file, wallpaper_folder, force)
            if verbose:
                print(f'{file}: {aspect}')
    return 0


def mainargs(argv=None):
    pser = argparse.ArgumentParser()
    pser.add_argument('file')
    pser.add_argument('wallpaper_folder')
    pser.add_argument('-a', '--aspect-min', type=float, default=1, dest='min_aspect')
    pser.add_argument('--aspect-max', type=float, default=999, dest='max_aspect')
    pser.add_argument('-n', '--dry-run', action='store_true')
    pser.add_argument('-v', '--verbose', action='store_true')
    pser.add_argument('-r', '--recurse', action='store_true')
    pser.add_argument('-f', '--force', action='store_true')
    args = pser.parse_args(argv)
    return vars(args)


if __name__ == "__main__":
    sys.exit(main(**mainargs()))
