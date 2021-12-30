import busio
import adafruit_ssd1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from board import SCL, SDA
from menu.menu import Menu
from menu.menu_renderer_config import MenuRendererConfig
import math
import itertools


class MenuRenderer:
    message = ""

    def __init__(self, menu: Menu, config: MenuRendererConfig):
        self.menu = menu
        self.config = config
        i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(config.width, config.height, i2c, addr=config.ssd1306_i2c_address)
        self.disp.fill(0)
        self.disp.show()
        self.image = Image.new('1', (self.disp.width, self.disp.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype(config.font_path, size=config.font_size)
        font_width, self.font_height = self.font.getsize("ABCabc")  # just a sample text to work with the font height
        self.cursor_position = 0
        self.frame_start_row = 0

    def rows_per_screen(self):
        rows = self.disp.height / self.font_height
        return math.floor(rows)

    def draw_row(self, row_number: int, text: str, selected: bool):
        x = 0
        y = row_number*self.font_height
        if selected:
            selection_extension = 0
            if row_number < self.rows_per_screen():
                selection_extension = self.config.row_selection_pixel_extension
            self.draw.rectangle((x, y, self.disp.width, y+self.config.font_size+selection_extension), outline=0,
                                fill=255)
            self.draw.text((x, y), text, font=self.font, spacing=0, stroke_fill=0, fill=0)
        else:
            self.draw.text((x, y), text, font=self.font, spacing=0, stroke_fill=0, fill=255)

    def draw_fullsceen_message(self, text: str):
        font_width, font_height = self.font.getsize(text)
        centered_width = (self.disp.width - font_width) / 2
        centered_height = (self.disp.height - font_height) / 2

        self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=255)
        self.draw.text((centered_width, centered_height), text, align="center", font=self.font,
                       stroke_fill=0, fill=0, textsize=20)

    def draw_menu(self):
        if self.menu.item_selection >= self.frame_start_row+self.rows_per_screen():
            self.frame_start_row = self.menu.item_selection + 1 - self.rows_per_screen()

        if self.menu.item_selection <= self.frame_start_row:
            self.frame_start_row = self.menu.item_selection

        # print("frame start: " + str(self.frame_start_row))
        # print("frame end: " + str(self.frame_start_row+self.rows_per_screen()))
        # print("position in menu: " + str(self.menu.item_selection))

        self.draw_menu_frame(self.frame_start_row, self.frame_start_row+self.rows_per_screen())

    def draw_menu_frame(self, frame_start_row: int, frame_end_row: int):
        self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
        row_on_screen = 0
        row_in_menuitems = frame_start_row
        for menuEntry in itertools.islice(self.menu.entries, frame_start_row, frame_end_row):
            if row_in_menuitems == self.menu.item_selection:
                self.draw_row(row_on_screen, menuEntry, True)
            else:
                self.draw_row(row_on_screen, menuEntry, False)
            row_in_menuitems += 1
            row_on_screen += 1
            if row_on_screen >= self.rows_per_screen():
                break

    def render(self):
        self.disp.fill(0)

        if self.message != "":
            self.draw_fullsceen_message(self.message)
        else:
            self.draw_menu()

        self.disp.image(self.image)
        self.disp.show()
