#!/usr/bin/env python

import time

from hx711 import HX711
from oled import OledDisplay

# Raspberry Pi pin configuration:
# HX711 pins
DATA_PIN = 9
CLOCK_PIN = 11


def main():
    hx = HX711(DATA_PIN, CLOCK_PIN)
    # Calibrate based on experiments with 1, 2, and 4 kg of water.
    hx.reference_unit = 21666.0

    hx.reset()
    hx.tare()

    disp = OledDisplay()

    while True:
        try:
            val = hx.get_weight(5)

            msg = '{:.1f} kg'.format(val)
            disp.display(msg)
            print(val)
            hx.power_down()
            hx.power_up()
            time.sleep(1)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
