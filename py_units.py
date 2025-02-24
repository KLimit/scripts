from functools import wraps

from quantiphy import Quantity


def unitter(unit):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            real = func(*args, **kwargs)
            return Quantity(real, unit)
        return wrapped
    return decorator
