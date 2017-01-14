#!/usr/bin/env python

import time
from hx711 import HX711


DATA_PIN = 9
CLOCK_PIN = 11
hx = HX711(DATA_PIN, CLOCK_PIN)

# Calibrate based on experiments with 1, 2, and 4 kg of water.
hx.reference_unit = 21666.0

hx.reset()
hx.tare()

while True:
    try:
        val = hx.get_weight(5)
        print(val)
        hx.power_down()
        hx.power_up()
        time.sleep(0.5)
    except KeyboardInterrupt:
        break
