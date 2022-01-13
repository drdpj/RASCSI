from luma.core.interface.serial import i2c
from menu.menu_renderer import MenuRenderer


class MenuRendererLumaOled(MenuRenderer):

    def display_init(self):
        serial = i2c(port=self._config.i2c_port, address=self._config.i2c_address)
        import luma.oled.device
        device = getattr(luma.oled.device, self._config.display_type)

        self.disp = device(serial_interface=serial,
                           rotate=self._config.get_mapped_rotation())

        print("Detected screen width: " + str(self.disp.width))
        print("Detected screen height: " + str(self.disp.height))

        self.disp.clear()
        self.disp.show()

        return self.disp

    def update_display_image(self, image):
        self.disp.display(self.image)
        self.disp.show()

    def update_display(self):
        self.disp.show()

    def display_clear(self):
        pass
        # self.disp.clear()
        # with canvas(self.disp) as draw:
        #     draw.rectangle((0, 0, self.disp.width-1, self.disp.height-1), outline=0, fill=0)
