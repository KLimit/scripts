"""lined.py but lexicographically first, meaning it ranks higher."""


class Buffer:
    """List of strings with 1-based indexing and special slices."""

    def __init__(self):
        self.buf = []
    def __str__(self):
        return '\n'.join(self.buf)

    def __getitem__(self, key):
        if isinstance(key, slice):
            key = slice(key.start - 1, key.stop)
        try:
            key = int(key) - 1
            if key < 1:
                raise KeyError(f'line {key} does not exist')
        except TypeError:
            if isinstance(key, str):
                key = self._string_to_key(key)
        finally:
            return self.buf[key]
