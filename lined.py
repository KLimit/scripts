"""Someday line editor in python."""
from io import StringIO


class Editor:
    insert_prompt = ''
    prompt = '> '
    stopchar = '.'
    address_delim = ','
    def __init__(self, buffer=None):
        if buffer is None:
            self.buffer = []
        self.address = 0
        self.urstack = UndoRedo()
        self.changed = False

    def read(self, filename):
        self.filename = filename
        with open(filename) as f:
            self.buffer = f.read().splitlines()

    def write(self, filename=None):
        # TODO: implement "atomic" write
        if filename is None:
            filename = self.filename
        with open(filename, 'w') as f:
            for line in self.buffer:
                print(line, file=f)
        self.changed = False

    def print(self, start=0, end=None):
        for line in self.buffer[slice(start, end)]:
            print(line)

    def numbered_print(self, start=0, end=None):
        longest = end
        if end == -1:
            longest = len(self.buffer)
        longest = len(str(longest))
        for n, line in enumerate(self.buffer[slice(start, end)], start=start or 0):
            print(f'{n:<{longest+2}}{line}')

    def insertmode(self, address=None):
        try:
            self._insertmode(address)
        except KeyboardInterrupt:
            return

    def _insertmode(self, address=None):
        if address is None:
            address = self.address
        insertbuf = []
        while (line := input(self.insert_prompt)) != self.stopchar:
            # print(line, file=insertbuf())
            insertbuf.append(line)
        self.insertlines(insertbuf, address)

    def normalmode(self):
        quit = False
        while not quit:
            quit = self.command(input(self.prompt))
            if quit and self.changed:
                c = input("buffer not written; quit anyway? ('y' to quit) ")
                if c.casefold() != 'y'.casefold():
                    quit = False

    def command(self, line):
        if not line:
            return
        command, *argv = line.split()
        *address, command = command
        # TODO: implement seperate range and address parsing
        # CONSIDER: subclass Editor that takes different address/range args
        if not address:
            address = ''
        else:
            address = address.pop()
        if address.endswith('w') and command == 'q':
            address = address[:-1]
            command = 'wq'
        start, _, end = address.partition(self.address_delim)
        if end == '$' or not end:
            end = None
        else:
            end = int(end)
        if not start:
            start = None
        else:
            start = int(start)
        match command:
            case 'r':
                self.read(*argv)
            case 'w':
                self.write(*argv)
            case 'wq':
                self.write(*argv)
                return True
            case 'q':
                return True
            case 'p':
                self.print(start, end)
            case 'n':
                self.numbered_print(start, end)
            case 'a':
                self.insertmode(start)
            case 'i':
                # WARN: doesn't insert correctly
                self.insertmode(start if start is None else start-1)
            case 'd':
                n = (len(self.buffer) if end is None else end) - (start or 0)
                self.deletelines(n, start)
            case 'u':
                try:
                    self.undo()
                except IndexError:
                    print('nothing to undo')
            case 'y':
                try:
                    self.redo()
                except IndexError:
                    print('already at newest change')
            case _:
                print('?')

    # these should maybe be in a buffer class or something
    def insertlines(self, lines, address):
        self.buffer = self.buffer[slice(None, address)] + lines + self.buffer[slice(address, None)]
        self.urstack.undo_append((self.deletelines, len(lines), address))
        self.changed = True
        self.address = address + len(lines)

    def deletelines(self, numlines, address):
        deleted = []
        try:
            for _ in range(numlines):
                deleted.append(self.buffer.pop(address))
        # slicing l[i:j] where j is beyond len(l) will replace j with  len(l)
        except IndexError:
            pass
        self.buffer = self.buffer[:address] + self.buffer[(address + numlines):]
        self.urstack.undo_append((self.insertlines, deleted, address))
        self.changed = True

    def undo(self):
        # it's up to the method that pushes to the undostack to add the correct
        # means of undoing itself
        method, *args = self.urstack.undo_pop()
        method(*args)
        # the undo action will append its own means of undoing back to the
        # undostack, but it really should go to the redostack
        self.urstack.redo_append(self.urstack.undo_pop())

    def redo(self):
        method, *args = self.urstack.redo_pop()
        method(*args)



class UndoRedo:
    def __init__(self):
        self.undostack = []
        self.redostack = []
    def undo_append(self, item):
        self.undostack.append(item)
        self.redostack.clear()
    def undo_pop(self, index=-1):
        return self.undostack.pop(index)
    def redo_append(self, item):
        self.redostack.append(item)
    def redo_pop(self, index=-1):
        return self.redostack.pop(index)


if __name__ == '__main__':
    ed = Editor()
    ed.normalmode()
