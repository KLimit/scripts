"""
Short script for Pratyush to more easily use the MTB to apply analog voltages.

henry.limm@motivps.com
2022 April
"""

from motiv_python_utils.automated_test import modular_test_board


def main():
    """Run a loop that asks for pin and then voltage."""
    mtb = modular_test_board.ModularTestBoard()
    print('CTRL-C to exit')
    while True:
        pin = raw_input('What pin? ')
        voltage = raw_input('What voltage? ')
        try:
            pin = int(pin)
            voltage = float(voltage)
        except ValueError:
            print('That pin or voltage was not valid.')
            continue
        singlevoltage(pin, voltage, mtb)


def singlevoltage(pin, voltage, mtb):
    """Set voltage given a pin using mtb."""
    mtb.select_input_pin(pin, maxVoltage=voltage)
    mtb.write_voltage(voltage)


if __name__ == '__main__':
    main()
