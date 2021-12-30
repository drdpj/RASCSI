import time
import observer
from board import SCL, SDA
import busio
import adafruit_ssd1306

from typing import List
from ctrlboard import AttributedButton, CtrlBoard
from encoder import Encoder

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class ButtonPressPrinter(observer.Observer):
    def update(self, updated_object):
        if isinstance(updated_object, AttributedButton):
            print(updated_object.name + " has been pressed!")
        if isinstance(updated_object, Encoder):
            print(updated_object.scaled_pos)


class Menu:
    entries: List = []
    item_selection = 0

    def add_entry(self, text):
        self.entries.append(text)


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
        self.font = ImageFont.truetype('fonts/SourceCodePro-Bold.ttf', 12)

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


class CtrlBoardMenuRenderer(MenuRenderer, observer.Observer):
    def update(self, updated_object):
        if isinstance(updated_object, AttributedButton):
            # print(updated_object.name + " has been pressed!")
            self.message = updated_object.name + " pressed!"
            self.render()
            time.sleep(1)
            self.message = ""
            self.render()
        if isinstance(updated_object, Encoder):
            # print(updatedObject.direction)
            if updated_object.direction == 1:
                self.menu.item_selection += 1
            if updated_object.direction == -1:
                self.menu.item_selection -= 1
            self.render()


#############################################
# Main
#############################################

def main():
    ctrlboard = CtrlBoard()

    menu = Menu()
    menu.add_entry("Hello")
    menu.add_entry("Foo")
    menu.add_entry("Bar")
    menu.add_entry("This")
    menu.add_entry("is")
    # menu.addEntry("a")
    # menu.addEntry("test")

    menu_renderer = CtrlBoardMenuRenderer(menu)
    ctrlboard.attach(menu_renderer)

    # button_press_printer = ButtonPressPrinter()
    # ctrlboard.attach(button_press_printer)

    menu_renderer.render()
    while True:
        ctrlboard.process_events()


if __name__ == '__main__':
    main()
