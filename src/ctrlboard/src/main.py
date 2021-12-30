from ctrlboard_hw.ctrlboard_hw import CtrlBoardHardware
from ctrlboard_hw.ctrlboard_hw_constants import CtrlBoardHardwareConstants
from menu.menu import Menu
from ctrlboard_event_handler.ctrlboard_menu_update_event_handler import CtrlBoardMenuUpdateEventHandler
# from ctrlboard_event_handler.ctrlboard_print_event_handler import CtrlBoardPrintEventHandler
from menu.menu_renderer import MenuRenderer
from menu.menu_renderer_config import MenuRendererConfig


def main():
    ctrlboard_hw = CtrlBoardHardware()

    menu = Menu()
    menu.add_entry("Hello")
    menu.add_entry("Foo")
    menu.add_entry("Bar")
    menu.add_entry("This")
    menu.add_entry("is")
    menu.add_entry("a")
    menu.add_entry("test")
    menu.add_entry("that")
    menu.add_entry("is")
    menu.add_entry("long")
    menu.add_entry("enough")
    menu.add_entry("for")
    menu.add_entry("scrolling")

    menu_renderer_config = MenuRendererConfig()
    menu_renderer_config.ssd1306_i2c_address = CtrlBoardHardwareConstants.SSD1306_I2C_ADDRESS
    menu_renderer = MenuRenderer(menu, menu_renderer_config)
    menu_update_event_handler = CtrlBoardMenuUpdateEventHandler(menu_renderer)
    ctrlboard_hw.attach(menu_update_event_handler)

    # print_event_handler = CtrlBoardPrintEventHandler()
    # ctrlboard_hw.attach(print_event_handler)

    menu_renderer.render()
    while True:
        ctrlboard_hw.process_events()


if __name__ == '__main__':
    main()
