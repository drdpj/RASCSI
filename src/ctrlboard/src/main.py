from ctrlboard_hw.ctrlboard_hw import CtrlBoardHardware
from ctrlboard_hw.ctrlboard_hw_constants import CtrlBoardHardwareConstants
from ctrlboard_event_handler.ctrlboard_menu_update_event_handler import CtrlBoardMenuUpdateEventHandler
# from ctrlboard_event_handler.ctrlboard_print_event_handler import CtrlBoardPrintEventHandler
from ctrlboard_menu_builder import CtrlBoardMenuBuilder
from menu.menu_controller import MenuController
from menu.menu_renderer_config import MenuRendererConfig
from rascsi_client import RaScsiClient
from socket_cmds import SocketTools


def main():
    ctrlboard_hw = CtrlBoardHardware()
    rascsi_client = RaScsiClient(SocketTools(), 'localhost', 6868)

    menu_renderer_config = MenuRendererConfig()
    menu_renderer_config.ssd1306_i2c_address = CtrlBoardHardwareConstants.SSD1306_I2C_ADDRESS

    menu_builder = CtrlBoardMenuBuilder(rascsi_client)
    menu_controller = MenuController(menu_builder)
    menu_controller.add(CtrlBoardMenuBuilder.SCSI_ID_MENU)
    menu_controller.add(CtrlBoardMenuBuilder.ACTION_MENU)

    menu_update_event_handler = CtrlBoardMenuUpdateEventHandler(menu_controller)
    ctrlboard_hw.attach(menu_update_event_handler)

    menu_controller.set_active_menu(CtrlBoardMenuBuilder.SCSI_ID_MENU)

    # menu_controller = MenuController(menu_renderer=menu_renderer)
    # print_event_handler = CtrlBoardPrintEventHandler()
    # ctrlboard_hw.attach(print_event_handler)

    while True:
        ctrlboard_hw.process_events()


if __name__ == '__main__':
    main()
