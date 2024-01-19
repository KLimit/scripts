#!/usr/bin/python3
"""Tool for calculating the regulated output voltage for ONSEMI LM2931AC parts.

Per the datasheet:
    V_out = V_ref * (1 + R2/R1)
Note that R1 and R2 are only used in ratio, so you can omit orders of magnitude
as necessary.

@auth henry.limm@motivps.com
@date 2022 October
"""

import argparse


def v_out(r1, r2, v_ref=1.20):
    """Calculate Vout per the LM2931 datasheet."""
    return v_ref * (1 + r2/r1)


if __name__ == '__main__':
    PSER = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    PSER.add_argument(
        'r1',
        type=float,
        help='top of divider'
    )
    PSER.add_argument(
        'r2',
        type=float,
        help='bottom of divider'
    )
    PSER.add_argument(
        '-r',
        '--v-ref',
        type=float,
        dest='v_ref',
        default=1.20,
        help='voltage at the adjust pin'
    )
    for arg, val in (('minimum', 1.17), ('nominal', 1.20), ('maximum', 1.23)):
        PSER.add_argument(
            f'--{arg}',
            action='store_const',
            dest='v_ref',
            const=val,
            help=f'V_out with {arg} adjust pin voltage ({val} V)',
        )
    print(v_out(**vars(PSER.parse_args())))
