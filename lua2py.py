"""Small utility for converting Lua-like tables into Python dicts and lists.

Useful in conjunction with something like lupa.
"""


def luatable2list(obj):
    """Convert dicts whose keys are integer strings starting from 1 into lists."""
    try:
        keys = obj.keys()
        keys = [int(key) for key in keys]
        if keys == list(range(1, len(keys)+1)):
            obj = list(obj.values())
    except  (ValueError, AttributeError):
        pass
    return obj


def lua2py(obj):
    """Try to convert a Lua-table-like into dicts and lists."""
    newdict = {}
    try:
        for key, value in obj.items():
            newdict[key] = luatable2list(lua2py(value))
    except AttributeError:
        return obj
    # try converting the topmost table as well
    return luatabletolist(newdict)
