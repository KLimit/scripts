#!/usr/bin/env python3
"""Get machine info from COFF header or PE type based on optional header."""
from collections import namedtuple
import struct


COFF_Header = namedtuple('COFF_Header', (
        'machine',
        'numberofsections',
        'timedatestamp',
        'pointertosymboltable',
        'numberofsymbols',
        'sizeofoptionalheader',
        'characteristics',
    ),
)


def main(infile):
    with open(infile, 'rb') as pe:
        pe.seek(PE_OFFSET_LOCATION)
        pe_offset = struct.unpack('I', pe.read(4))[0]
        pe.seek(pe_offset + len(PE_SIGNATURE))
        coff_header = pe.read(struct.calcsize(COFF_HEADER_F))
    coff_header = COFF_Header(*struct.unpack(COFF_HEADER_F, coff_header))
    print(MACHINE_TYPES[coff_header.machine])


def mainargs(argv=None):
    import argparse
    pser = argparse.ArgumentParser()
    pser.add_argument('infile')
    args = pser.parse_args(argv)
    return vars(args)


PE_OFFSET_LOCATION = 0x3c
PE_SIGNATURE = b'PE\0\0'
COFF_HEADER_F = 'HHIIIHH'
# OPTIONAL_HEADER = {
#     0x10b: "PE32",
#     0x20b: "PE32+",
# }


MACHINE_TYPES = {
    0x0: "UNKNOWN",
    0x184: "ALPHA",
    0x284: "ALPHA64",
    0x1d3: "AM33",
    0x8664: "AMD64",
    0x1c0: "ARM",
    0xaa64: "ARM64",
    0x1c4: "ARMNT",
    0x284: "AXP64",
    0xebc: "EBC",
    0x14c: "I386",
    0x200: "IA64",
    0x6232: "LOONGARCH32",
    0x6264: "LOONGARCH64",
    0x9041: "M32R",
    0x266: "MIPS16",
    0x366: "MIPSFPU",
    0x466: "MIPSFPU16",
    0x1f0: "POWERPC",
    0x1f1: "POWERPCFP",
    0x166: "R4000",
    0x5032: "RISCV32",
    0x5064: "RISCV64",
    0x5128: "RISCV128",
    0x1a2: "SH3",
    0x1a3: "SH3DSP",
    0x1a6: "SH4",
    0x1a8: "SH5",
    0x1c2: "THUMB",
    0x169: "WCEMIPSV2",
}


if __name__ == "__main__":
    import sys
    sys.exit(main(**mainargs()))
