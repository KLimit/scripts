"""Super Python EDitor.

I'm just making up names, now.
"""
import cmd


class Editor(cmd.Cmd):
    def __init__(self):
        self.buffer = []
    def print(self, start=None, end=None):
        for line in self.buffer[slice(start=start, end=end)]:
            print(line)


def add_cmd(func):
    def cmd(*args, **kwargs):
        pass

