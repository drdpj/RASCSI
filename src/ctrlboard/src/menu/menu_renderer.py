import busio
import adafruit_ssd1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from board import SCL, SDA


class MenuRenderer:
    message = ""

    def __init__(self, menu):
        self.menu = menu
        i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
        self.disp.fill(0)
        self.disp.show()
        self.image = Image.new('1', (self.disp.width, self.disp.height))
        self.draw = ImageDraw.Draw(self.image)

        # self.font = ImageFont.truetype('fonts/DejaVuSansMono-Bold.ttf', 12)
        self.font = ImageFont.truetype('resources/SourceCodePro-Bold.ttf', 12)

    def render(self):
        i = 0
        padding = -2
        top = padding
        x = 0

        self.disp.fill(0)
        if self.message != "":
            self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=255)
            self.draw.text((x, top + 2 * 12), self.message, font=self.font, stroke_fill=0, fill=0, textsize=20)
            self.disp.image(self.image)
            self.disp.show()
            return

        self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
        for menuEntry in self.menu.entries:
            if i == self.menu.item_selection:
                self.draw.rectangle((x, top + i * 12, self.disp.width, top + (i + 1) * 12), outline=0, fill=255)
                self.draw.text((x, top + i * 12), menuEntry, font=self.font, stroke_fill=0, fill=0, textsize=20)
            else:
                self.draw.text((x, top + i * 12), menuEntry, font=self.font, stroke_fill=0, fill=255, textsize=20)

            i += 1

        self.disp.image(self.image)
        self.disp.show()
