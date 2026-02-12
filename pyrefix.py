#!/usr/bin/env python3
"""Integer and float literals with SI prefixes.

Of course, they are after the number, but they would prefix a unit.
"""
import collections.abc

try:
    from ideas import import_hook
    import token_utils
    _has_ideas = True
except ImportError:
    _has_ideas = False


class AliasDict(collections.abc.MutableMapping):
    def __init__(self, *args, aliases=None, **kwargs):
        self.dict = dict(*args, **kwargs)
        self._aliases = aliases or {}
    def alias(self, key, alias, strict=True):
        """Alias the `alias` the `key`."""
        if key not in self and strict:
            raise KeyError('Cannot make an alias to a nonexistent key')
        self._aliases[alias] = key
    def __getitem__(self, key):
        key = self._aliases.get(key, key)
        return self.dict[key]
    def __setitem__(self, key, value):
        key = self._aliases.get(key, key)
        self.dict[key] = value
    def __delitem__(self, key):
        key = self._aliases.pop(key, key)
        del self.dict[key]
    def __iter__(self):
        return iter(self.dict)
    def __len__(self):
        return len(self.dict)
    def __repr__(self):
        repr = f'{type(self).__qualname__}{self.dict!r}'
        if self._aliases:
            repr += f', aliases{self._aliases!r}'
        return repr


magnitudes = AliasDict(
    (
        (symbol, power)
        for symbol, power
        in zip(
            'qryzafpnum_kMGTPEZYRQ',
            range(-30, 31, 3),
        )
        if power  # skip 1e0
    ),
    aliases={'µ': 'u'},
)
imaginary = 'j'


if _has_ideas:
    import itertools

    def transform_source(source, **kwargs):
        # TODO: review the auto_self example and reconstruct the lines so that
        # we can untokenize tokens rather than their strings.
        tokens = token_utils.tokenize(source)
        new_tokens = []
        skipnow = False
        # for prev, now in itertools.pairwise(itertools.chain([None], tokens)):
        for now, next in itertools.pairwise(tokens):
            if skipnow:
                skipnow = False
                continue
            if now.is_number() and next.is_name():
                prefix = next.string
                if is_imaginary := prefix.endswith(imaginary):
                    prefix = next.string[:-1]
                if prefix in magnitudes:
                    now.string += f'e{magnitudes[prefix]}'
                    now.string += imaginary if is_imaginary else ''
                    skipnow = True
            new_tokens.append(now)
        if not skipnow:
            new_tokens.append(next)
        # use t.string because untokenize will insert parts of the original
        # line if the tokens' lengths/positions aren't modified
        return token_utils.untokenize(t.string for t in new_tokens)


    def add_hook(**kwargs):
        """Create and automatically add the import hoook in sys.meta_path."""
        return import_hook.create_hook(
            transform_source=transform_source,
            hook_name=__name__,
        )
