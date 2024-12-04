import enum
import sys

auto = enum.auto

def global_enum(cls, update_str=False):
    cls.__repr__ = global_enum_repr
    if update_str:
        cls.__str__ = global_str
    sys.modules[cls.__module__].__dict__.update(cls.__members__)
    return cls

def noupdates(cls):
    sys.modules[cls.__module__].__dict__.update(cls.__members__)
    return cls

def global_enum_repr(self):
    module = self.__class__.__module__.split('.')[-1]
    return '%s.%s' % (module, self._name_)

def global_str(self):
    if self._name_ is None:
        cls_name = self.__class__.__name__
        return "%s(%r)" % (cls_name, self._value_)
    else:
        return self._name_

class StrEnum(enum.Enum):
    __str__ = str.__str__
    __format__ = str.__format__

@global_enum
class GNLOGL(str, StrEnum):
    ONE = 'one'
    TWO = 'two'
    THREE = 'three'
    FMT = 'hello {}'

@noupdates
class LG(str, StrEnum):
    ON = 'o'
    DU = 't'
    TO = 's'

class PO(str, StrEnum):
    ONE = 'one'
    TWO = 'two'
    THREE = 'three'
    FMT = 'hello {}'
