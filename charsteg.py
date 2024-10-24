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
def stegan_encode(plaintext, character, blocks=3, fill=True, lines=True, seed=None):
    if seed is not None:
        random.seed(seed)
    plaintext = [ord(ch.upper()) - ord('A') for ch in plaintext if ch in string.ascii_letters]
    if fill:
        filler = CharSource(character)
    else:
        filler = RandSource(' ')
    nextblock = lambda: random.choice(range(blocks))
    positions = [
        pos + 26 * nextblock()
        for pos in plaintext
    ]
    width = 26 * blocks
    steg = ''
    for n, pos in enumerate(positions):
        for _ in range(pos):
            steg += next(filler)
        steg += character
        for _ in range(pos+1, width):
            steg += next(filler)
        if lines:
            steg += '\n'
    random.seed()
    # don't want trailing newline
    if lines:
        steg = steg[:-1]
    return steg
def stegan_decode(stegtext: str, character):
    stegtext = stegtext.replace('\n', '')
    indices = [
        n
        for n, ch in enumerate(stegtext)
        if ch == character
    ]
    characters = [
        chr(n%26 + ord('A'))
        for n in indices
    ]
    return ''.join(characters)

def main():
    import sys
    if len(sys.argv) == 1:
        print('usage: charsteg encode|decode character', file=sys.stderr)
        print('text is read from stdin', file=sys.stderr)
        sys.exit()
    if len(sys.argv) != 3:
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
    print(func(text, char))


if __name__ == '__main__':
    main()
