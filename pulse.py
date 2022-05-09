#!/usr/bin/sh python3
"""
Invoke my Pulse VPN program after asking for password.

henry
"""

import argparse
import getpass
import subprocess


def main():
    """Get username and password."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logoff', action='store_true')
    args = parser.parse_args()
    url = 'https://mag.motivps.com'
    realm = 'motivps-ad-realm'
    progdir = 'C:/Program Files (x86)/Common Files/Pulse Secure/Integration/'
    prog = 'pulselauncher.exe'

    usr = getpass.getuser()
    pwd = getpass.getpass()

    call = [
        progdir + prog,
        f'-url {url}',
        f'-u {usr}',
        f'-p {pwd}',
        f'-r {realm}',
    ]
    if args.logoff:
        call.append('-signout')

    print(call)

    subprocess.call(call)


if __name__ == '__main__':
    main()
