import hashlib
from getpass import getpass

getpass_prompt = 'Password: '
def gethash(prompt=getpass_prompt, prefix=''):
    if prefix:
        print(prefix, end='', flush=True)
    # not really sure whether blake2b is the "correct" way to do this
    h = hashlib.blake2b(getpass(prompt).encode())
    return h.digest()


def test(target, prompt=getpass_prompt, prefix=''):
    return gethash(prompt, prefix) == target


if __name__ == '__main__':
    target = False
    while not target:
        target = gethash('Password to practice: ')
        if not test(target, prompt='Enter again to confirm: '):
            target = False
            print('Passwords did not match; try again')
    n = 0
    while True:
        print('correct' if test(target, prefix=f'{n} ') else 'wrong')
        n += 1
