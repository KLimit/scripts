#!/usr/bin/env python3
import argparse
import ast
import sys

Assign = ast.Assign
FunctionDef = ast.FunctionDef
Lambda = ast.Lambda

class Comparer:
    args_name = 'args'
    kwargs_name = 'kwargs'
    outfmt_name = 'outfmt'

    def __init__(self, src, args=None, kwargs=None):
        src = ast.parse(src)
        callablenodes = []
        for node in src.body:
            match node, getattr(node, 'value', None), getattr(node, 'targets', None):
                case (FunctionDef(), _, targets) | (Assign(), Lambda(), targets):
                    # TODO: use prevous callablenode when it's an output format
                    callablenodes.append(makecallable(node, ))
                case (Assign(), (ast.List() | ast.Tuple() | ast.Dict()), targets):
                    targetname = targets[0].id
                    if targetname in (self.args_name, self.kwargs_name):
                        setattr(self, targetname, ast.literal_eval(node.value))
        # TODO: get rid of output format requirement; probably
        for node in callablenodes:
            pass
        if args is not None:
            self.args = args
        if kwargs is not None:
            self.kwargs = kwargs


def makecallable(node, name=None):
    if isinstance(node, FunctionDef):
        name = node.name
    elif isinstance(node, Assign) and isinstance(node.value, Lambda):
        name = node.targets[0].id
    else:
        raise ValueError('node must be a callable thing')
    module = ast.Module([node], type_ignores=[])
    code = compile(module, name, 'exec')
    module_namespace = {}
    exec(code, module_namespace)
    if isinstance(node, Lambda):
        module_namespace[node.name]
    return module_namespace[node.name]


def main(src):
    src = ast.parse(src)
    return 0


def mainargs(argv=None):
    pser = argparse.ArgumentParser()
    args = pser.parse_args(argv)
    return vars(args)


if __name__ == "__main__":
    sys.exit(main(**mainargs()))
