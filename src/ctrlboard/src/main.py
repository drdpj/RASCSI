from ctrlboard_hw.ctrlboard_hw import CtrlBoardHardware
from menu.menu import Menu
from ctrlboard_event_handler.ctrlboard_menu_update_event_handler import CtrlBoardMenuUpdateEventHandler
# from ctrlboard_event_handler.ctrlboard_print_event_handler import CtrlBoardPrintEventHandler


def main():
    ctrlboard_hw = CtrlBoardHardware()

    menu = Menu()
    menu.add_entry("Hello")
    menu.add_entry("Foo")
    menu.add_entry("Bar")
    menu.add_entry("This")
    menu.add_entry("is")
    # menu.addEntry("a")
    # menu.addEntry("test")

    menu_renderer = CtrlBoardMenuUpdateEventHandler(menu)
    ctrlboard_hw.attach(menu_renderer)

    # print_event_handler = CtrlBoardPrintEventHandler()
    # ctrlboard_hw.attach(print_event_handler)

    menu_renderer.render()
    while True:
        ctrlboard_hw.process_events()


if __name__ == '__main__':
    main()
