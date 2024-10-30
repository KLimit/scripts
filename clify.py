#!/usr/bin/env python3
from argparse import ArgumentParser
import atexit
import inspect

# from IPython.core.debugger import set_trace as breakpoint
# from IPython import embed


def clify(fn):
    def cliwrapped(argv=None):
        pser = ArgumentParser()
        sig = inspect.signature(fn)
        for param in sig.parameters.values():
            names, pser_kwargs = param_to_arg(param)
            pser.add_argument(*names, **pser_kwargs)
        try:
            args = pser.parse_args(argv)
        except SystemExit:
            return
        return fn(**vars(args))
    # in lieu of monkeypatching the module, call at exit
    if fn.__module__ == '__main__':
        # calling_frame = inspect.currentframe().f_back
        # print(calling_frame)
        # breakpoint()
        # embed()
        atexit.register(cliwrapped)
    return fn


def param_to_arg(param: inspect.Parameter) -> (tuple, dict):
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
    elif has_default and param.default is not None:
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
