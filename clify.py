#!/usr/bin/env python3
from argparse import ArgumentParser
import atexit
import functools
import inspect

# from IPython.core.debugger import set_trace as breakpoint
# from IPython import embed


def _clify(fn, /, *, infer_type=True):
    def cliwrapped(argv=None):
        pser = ArgumentParser()
        sig = inspect.signature(fn)
        for param in sig.parameters.values():
            names, pser_kwargs = param_to_arg(param, infer_type=infer_type)
            pser.add_argument(*names, **pser_kwargs)
        try:
            args = pser.parse_args(argv)
        except SystemExit:
            return
        return fn(**vars(args))
    # in lieu of monkeypatching the module, call at exit
    if fn.__module__ == '__main__':
        atexit.register(cliwrapped)
    return fn

def clify(fn=None, /, *, infer_type=True):
    # copy pattern from dataclasses.py
    if fn is None:
        # called with parens
        return functools.partial(_clify, infer_type=infer_type)
    else:
        return _clify(fn)


def param_to_arg(param: inspect.Parameter, infer_type=True) -> (tuple, dict):
    kwargs = {}
    if (has_default := param.default is not param.empty):
        kwargs['help'] = "(default: %(default)s)"
        # assume that boolean defaults are meant to be used as flags
        if isinstance(param.default, bool):
            kwargs['action'] = 'store_false' if param.default else 'store_false'
        else:
            kwargs['default'] = param.default
    if param.annotation is not param.empty:
        kwargs['type'] = param.annotation
    elif has_default and param.default is not None and infer_type:
        # assume type to be type of the default value if not explicit
        # (when default value is given)
        kwargs['type'] = type(param.default)
    if param.kind == param.VAR_POSITIONAL:
        kwargs['nargs'] = '*'
    # optional arg or not
    if (
        (param.kind == param.KEYWORD_ONLY)
        or (has_default and param.kind != param.POSITIONAL_ONLY)
    ):
        strippedname = param.name.strip('_-')
        names = ('-' + strippedname[0], '--' + strippedname)
        kwargs['dest'] = param.name
    else:
        names = (param.name, )
    return names, kwargs
    # match param.kind:
    #     case param.POSITIONAL_ONLY: pass
    #     case param.POSITIONAL_OR_KEYWORD: pass
    #     case param.VAR_POSITIONAL:
    #         kwargs['nargs'] = '*'
    #     case param.KEYWORD_ONLY: pass
    #     case param.VAR_KEYWORD: pass
