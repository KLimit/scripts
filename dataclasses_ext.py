#!/usr/bin/env python3
from dataclasses import *
_dataclass = dataclass


def _process_class(
    cls,
    /,
    *,
    default=MISSING,
    default_factory=MISSING,
    annotation_as_factory=False,
    **kwargs,
):
    """Extend dataclass decorator with option for default field values."""
    if default_factory is not MISSING and annotation_as_factory:
        raise ValueError('cannot specify both default_factory and annotation_as_factory')
    fieldkwarg = {}
    if default is not MISSING:
        fieldkwarg['default'] = default
    if default_factory is not MISSING:
        fieldkwarg['default_factory'] = default_factory
    if fieldkwarg or annotation_as_factory:
        for attr, annotation in getattr(cls, '__annotations__', {}).items():
            if hasattr(cls, attr):
                continue
            if annotation_as_factory:
                fieldkwarg['default_factory'] = annotation
            setattr(cls, attr, field(**fieldkwarg))
    return _dataclass(cls, **kwargs)


def dataclass(cls=None, /, **kwargs):
    def wrap(cls):
        return _process_class(cls, **kwargs)
    if cls is None:
        return wrap
    return wrap(cls)
