from ctrlboard_event_handler.ctrlboard_test_menuitem_handler import CtrlBoardTestMenuItemHandler
from ctrlboard_hw.ctrlboard_hw import CtrlBoardHardware
from ctrlboard_hw.ctrlboard_hw_constants import CtrlBoardHardwareConstants
from menu.menu import Menu
from ctrlboard_event_handler.ctrlboard_menu_update_event_handler import CtrlBoardMenuUpdateEventHandler
# from ctrlboard_event_handler.ctrlboard_print_event_handler import CtrlBoardPrintEventHandler
from menu.menu_renderer import MenuRenderer
from menu.menu_renderer_config import MenuRendererConfig


def create_first_level_test_menu():
    menuhandler = CtrlBoardTestMenuItemHandler()
    menu = Menu()
    menu.add_entry("Hello dfsdf dsf sdfsdf s", menuhandler.transition_to_menu)
    menu.add_entry("Foo", menuhandler.transition_to_menu)
    menu.add_entry("Bar dfsdfsdf sdf sdfs f", menuhandler.print_item_text_to_stdout)
    menu.add_entry("This", menuhandler.print_item_text_to_stdout)
    menu.add_entry("is", menuhandler.print_item_text_to_stdout)
    menu.add_entry("a")
    menu.add_entry("test")
    menu.add_entry("that")
    menu.add_entry("is")
    menu.add_entry("long")
    menu.add_entry("enough")
    menu.add_entry("for")
    menu.add_entry("scrolling")
    return menu


def create_second_level_test_menu():
    # menuhandler = CtrlBoardTestMenuItemHandler()
    menu2 = Menu()
    menu2.add_entry("Return")
    menu2.add_entry("level")
    menu2.add_entry("of")
    menu2.add_entry("items")
    menu2.add_entry("and")
    menu2.add_entry("lots")
    menu2.add_entry("of")
    menu2.add_entry("them")
    menu2.add_entry("again")
    menu2.add_entry("to")
    menu2.add_entry("test")
    menu2.add_entry("stuff")
    return menu2


def main():
    ctrlboard_hw = CtrlBoardHardware()

    menu_renderer_config = MenuRendererConfig()
    menu_renderer_config.ssd1306_i2c_address = CtrlBoardHardwareConstants.SSD1306_I2C_ADDRESS

    first_level_menu = create_first_level_test_menu()
    second_level_menu = create_second_level_test_menu()

    second_menu_renderer = MenuRenderer(second_level_menu, menu_renderer_config)
    navigation_info = {"second_level_menu": second_level_menu, "second_level_menu_renderer": second_menu_renderer}

    menu_renderer = MenuRenderer(first_level_menu, menu_renderer_config)
    menu_update_event_handler = CtrlBoardMenuUpdateEventHandler(menu_renderer, navigation_info)
    ctrlboard_hw.attach(menu_update_event_handler)

    # print_event_handler = CtrlBoardPrintEventHandler()
    # ctrlboard_hw.attach(print_event_handler)

    menu_renderer.render()
    while True:
        ctrlboard_hw.process_events()


if __name__ == '__main__':
    main()
