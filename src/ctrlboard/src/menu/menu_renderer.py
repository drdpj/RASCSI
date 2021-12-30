import busio
import adafruit_ssd1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from board import SCL, SDA
from menu.menu import Menu
from menu.menu_renderer_config import MenuRendererConfig


class MenuRenderer:
    message = ""

    def __init__(self, menu: Menu, config: MenuRendererConfig):
        self.menu = menu
        i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(config.width, config.height, i2c, addr=config.ssd1306_i2c_address)
        self.disp.fill(0)
        self.disp.show()
        self.image = Image.new('1', (self.disp.width, self.disp.height))
        self.draw = ImageDraw.Draw(self.image)

        self.font = ImageFont.truetype(config.font_path, config.font_size)

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
