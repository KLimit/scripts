"""quick and dirty text steganography"""
import string
import random
class RandSource:
    def __init__(self, charset):
        self.charset = charset
    def __contains__(self, thing):
        return thing in self.charset
    def __next__(self):
        return random.choice(self.charset)

class CharSource(RandSource):
    def __init__(self, *exclude):
        charset = string.ascii_letters + string.digits + string.punctuation
        for ch in exclude:
            charset = charset.replace(ch, '')
        self.charset = charset
def toalpha(num, upper=True):
    offset = ord('A' if upper else 'a')
    return chr(num%26 + offset)
def to_ord(ch):
    return ord(ch.upper()) - ord('A')
def stegan_encode(
    plaintext,
    character,
    blocks=3,
    fill=True,
    keepspaces=True,
):
    if fill:
        filler = CharSource(character)
    else:
        filler = RandSource(' ')
    nextblock = lambda: random.choice(range(blocks))
    alph = lambda ch: ord(ch.upper()) - ord('A')
    positions = [
        -1 if ch == ' ' else alph(ch) + 26 * nextblock()
        for ch in plaintext
        if ch in string.ascii_letters + ' '
    ]
    width = 26 * blocks
    steg = ''
    for n, pos in enumerate(positions):
        if pos < 0:
            if keepspaces:
                for _ in range(width):
                    steg += next(filler)
                steg += '\n'
            continue
        for _ in range(pos):
            steg += next(filler)
        steg += character
        for _ in range(pos+1, width):
            steg += next(filler)
        steg += '\n'
    # don't want trailing newline
    return steg[:-1]
def stegan_decode(stegtext: str, character):
    lines = stegtext.splitlines()
    decoded = []
    for line in lines:
        indices = [
            n
            for n, ch in enumerate(line)
            if ch == character
        ]
        characters = [
            chr(n%26 + ord('A'))
            for n in indices
        ]
        line = ''.join(characters)
        if not line:
            line = ' '
        decoded.append(line)
    return ''.join(decoded)

def main():
    import sys
    if len(sys.argv) == 1:
        print('usage: charsteg encode|decode character', file=sys.stderr)
        print('text is read from stdin', file=sys.stderr)
        sys.exit()
    if len(sys.argv) not in (3, 4):
        print('must provide "encode"/"decode" and encoding character', file=sys.stderr)
        sys.exit(1)
    text = sys.stdin.read()
    if sys.argv[1] == 'encode':
        func = stegan_encode
    elif sys.argv[1] == 'decode':
        func = stegan_decode
    else:
        print(f'{sys.argv[1]} is not a valid option', file=sys.stderr)
        sys.exit(2)
    char = sys.argv[2]
    if len(char) != 1:
        print('"character" must be a single character', file=sys.stderr)
        sys.exit(3)
    try:
        random.seed(sys.argv[3])
    except IndexError:
        pass
    print(func(text, char))


if __name__ == '__main__':
    main()
