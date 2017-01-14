#!/usr/bin/env python

import time

import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from hx711 import HX711

# Raspberry Pi pin configuration:
# HX711 pins
DATA_PIN = 9
CLOCK_PIN = 11
# OLED PINS
RST_PIN = 24



def main():
    # 128x32 display with hardware I2C:
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST_PIN, i2c_address=0x3C)
    disp.begin()
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)

    hx = HX711(DATA_PIN, CLOCK_PIN)
    # Calibrate based on experiments with 1, 2, and 4 kg of water.
    hx.reference_unit = 21666.0

    hx.reset()
    hx.tare()

    while True:
        try:
            val = hx.get_weight(5)

            disp.clear()
            disp.display()
            image = Image.new('1', (width, height))
            draw = ImageDraw.Draw(image)
            msg = '{:.1f} kg'.format(val)
            w, h = draw.textsize(msg, font=font)
            draw.text(((width-w)/2,(height-h)/2), msg, font=font, fill=1)
            disp.image(image)
            disp.display()
            print(val)
            hx.power_down()
            hx.power_up()
            time.sleep(1)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
