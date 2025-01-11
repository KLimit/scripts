from collections import Counter
import itertools
from math import inf

import curses

from clify import clify


class SquareGrid:
    # How many times have I implemented a 2D array of cells?
    def __init__(self, size, default=None):
        self.size = size
        self.default = default
        self.grid = [[default for _ in range(size)] for _ in range(size)]
    def __getitem__(self, index):
        row, column = index
        return self.grid[row][column]
    def __setitem__(self, index, value):
        row, column = index
        self.grid[row][column] = value
    def __repr__(self):
        firstline = '[' + repr(self.grid[0])  # ]
        rest = '\n'.join(' ' + repr(row) for row in self.grid[1:]) + ']'
        return '\n'.join([firstline, rest])
    def flattened(self):
        return list(itertools.chain.from_iterable(self.grid))
    def __len__(self):
        return self.size**2
    def __iter__(self):
        yield from self.grid



def clip(a, min_, max_):
    return max(min(a, max_), min_)


class ClippedValue:
    def __init__(self, value, min=-inf, max=inf):
        self.value = value
        self.min = min
        self.max = max
    def __get__(self, obj, objtype=None):
        return self.value
    def __set__(self, obj, value):
        min = self.getattr('min', obj)
        max = self.getattr('max', obj)
        self.value = clip(value, min, max)
    def getattr(self, attr, obj):
        selfval = getattr(self, attr)
        try:
            return getattr(obj, selfval)
        except (TypeError, AttributeError):
            return selfval

class Puzzle:
    winrow = ClippedValue(0, 0, 'win_grid_max')
    wincol = ClippedValue(0, 0, 'win_grid_max')
    def __init__(self, size=3, windowsize=2):
        self.grid = SquareGrid(size, 0)
        self.gridsize = size
        self.winsize = windowsize
        self.win_grid_max = size - windowsize

    def cells_in_window(self):
        return (
            (row, column)
            for row in range(self.winrow, self.winrow + self.winsize)
            for column in range(self.wincol, self.wincol + self.winsize)
        )
    def values_in_window(self):
        return [self.grid[row, column] for row, column in self.cells_in_window()]

    def add_to_window(self, a=1):
        for cell in self.cells_in_window():
            self.grid[*cell] += a

    def move_window(self, row, column):
        self.winrow += row
        self.wincol += column

    def is_complete(self):
        return len(set(self.grid.flattened())) == len(self.grid)


class TrackingPuzzle(Puzzle):
    def __init__(self, size=3, windowsize=2):
        super().__init__(size, windowsize)
        self.undostack = []
        self.movecount = 0
    def add_to_window(self, a=1):
        super().add_to_window(a)
        self.movecount += a
        self.undostack.append(((self.winrow, self.wincol), a))
    def undo(self):
        try:
            (self.winrow, self.wincol), a = self.undostack.pop()
            self.add_to_window(-a)
            return self.undostack.pop()  # don't track the undo
        except IndexError:
            pass


class Game:
    def __init__(self, size, windowsize):
        self.puzzle = TrackingPuzzle(size, windowsize)
    def play(self, stdscr):
        stdscr.clear()
        curses.curs_set(0)
        self.draw_puzzle(stdscr)
        stdscr.refresh()
        while not self.puzzle.is_complete():
            try:
                key = stdscr.getkey()
            except KeyboardInterrupt:
                return
            match key:
                case 'h' | 'KEY_LEFT':
                    self.puzzle.move_window(0, -1)
                case 'j' | 'KEY_DOWN':
                    self.puzzle.move_window(1, 0)
                case 'k' | 'KEY_UP':
                    self.puzzle.move_window(-1, 0)
                case 'l' | 'KEY_RIGHT':
                    self.puzzle.move_window(0, 1)
                case '\n' | ' ':
                    self.puzzle.add_to_window()
                case 'u':
                    self.puzzle.undo()
                case 'q':
                    return
            self.draw_puzzle(stdscr, debug=False)
            stdscr.refresh()
        if self.puzzle.is_complete():
            stdscr.addstr(0, 0, self.statusbar + '; BOARD COMPLETE! (any key to quit)')
        stdscr.getkey()

    message = 'make all cells unique'
    @property
    def statusbar(self):
        return f'"q" to quit; "u" to undo; moves: {self.puzzle.movecount}'

    cellwidth = 4
    windowchar = '|'
    dupechar = '*'

    def draw_puzzle(self, window, debug=None):
        window.addstr(0, 0, self.statusbar)
        grid = self.puzzle.grid
        windowed_cells = list(self.puzzle.cells_in_window())
        dupes = get_duplicates(grid.flattened())
        if debug:
            print(f'{windowed_cells=}')
        for row, cells in enumerate(grid):
            for column, cell in enumerate(cells):
                if debug:
                    print(f'{row=}, {column=}')
                if (row, column) in self.puzzle.cells_in_window():
                    attrs = curses.A_BOLD | curses.A_UNDERLINE
                    fillchar = self.windowchar
                else:
                    attrs = 0
                    fillchar = ' '
                if cell in dupes:
                    cell = f'{self.dupechar}{cell}'
                value = f'{cell:{fillchar}^{self.cellwidth}}'
                # line, char for terminal
                line = 1 + row
                # one char of left pad, one char between each cell
                char = 1 + ((self.cellwidth + 1) * column)
                window.addstr(line, char, value, attrs)
        window.addstr(line + 1, 0, self.message)


def get_duplicates(seq):
    return [
        item
        for item, count in Counter(seq).items()
        if count > 1
    ]

@clify
def main(size=3, windowsize=2):
    game = Game(size, windowsize)
    curses.wrapper(game.play)
