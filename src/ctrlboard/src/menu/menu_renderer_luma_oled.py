from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106, ssd1306
from menu.menu_renderer import MenuRenderer


class MenuRendererLumaOled(MenuRenderer):

    def display_init(self):
        serial = i2c(port=1, address=self._config.ssd1306_i2c_address)
        self.disp = sh1106(serial_interface=serial, width=self._config.width, height=self._config.height,
                           rotate=self._config.get_mapped_rotation())
        # self.disp = ssd1306(serial_interface=serial, width=self._config.width, height=self._config.height,
        #                    rotate=self._config.get_mapped_rotation())

        self.disp.show()

        return self.disp

    def update_display_image(self, image):
        self.disp.display(self.image)
        self.disp.show()

    def update_display(self):
        self.disp.show()

    def display_clear(self):
        pass
        # with canvas(self.disp) as draw:
        #     draw.rectangle((0, 0, self.disp.width-1, self.disp.height-1), outline=0, fill=0)
