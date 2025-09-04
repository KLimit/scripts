#!/usr/bin/env python3
import contextlib
import io
import os
import shutil
import subprocess


def getpager():
    name = os.environ.get('pager', 'less')
    return shutil.which(name)


class Pager(contextlib.redirect_stdout):
    def __init__(self):
        super().__init__(io.StringIO())
    def __enter__(self):
        return super().__enter__()
    def __exit__(self, *args, **kwargs):
        super().__exit__(*args, **kwargs)
        page(self._new_target.getvalue())


contextsentinel = object()
def page(obj=contextsentinel, /):
    if obj is not contextsentinel:
        subprocess.run(
            getpager(),
            text=True,
            input=str(obj),
        )
    else:
        return Pager()
