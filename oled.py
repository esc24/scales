import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# OLED PINS
RST_PIN = 24


class OledDisplay:
    def __init__(self):
        # 128x32 display with hardware I2C:
        self.oled = Adafruit_SSD1306.SSD1306_128_32(rst=RST_PIN,
                                                    i2c_address=0x3C)
        self.oled.begin()
        self.oled.clear()
        self.oled.display()
        self.font = ImageFont.truetype(
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)

    def clear(self):
        self.oled.clear()
        self.oled.display()

    def display_error(self, msg):
        pass

    def display(self, msg):
        image = Image.new('1', (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)
        w, h = draw.textsize(msg, font=self.font)
        draw.text(((self.oled.width-w)/2,(self.oled.height-h)/2),
                  msg, font=self.font, fill=1)
        self.oled.image(image)
        self.oled.display()
