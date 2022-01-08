import argparse

from config import CtrlboardConfig
from ctrlboard_hw.ctrlboard_hw import CtrlBoardHardware
from ctrlboard_hw.ctrlboard_hw_constants import CtrlBoardHardwareConstants
from ctrlboard_event_handler.ctrlboard_menu_update_event_handler import CtrlBoardMenuUpdateEventHandler
# from ctrlboard_event_handler.ctrlboard_print_event_handler import CtrlBoardPrintEventHandler
from ctrlboard_menu_builder import CtrlBoardMenuBuilder
from menu.menu_controller import MenuController
from menu.menu_renderer_config import MenuRendererConfig
from rascsi_client import RaScsiClient
from socket_cmds import SocketTools


def parse_config():
    config = CtrlboardConfig()
    cmdline_args_parser = argparse.ArgumentParser(description='RaSCSI ctrlboard service')
    cmdline_args_parser.add_argument(
        "--rotation",
        type=int,
        choices=[0, 180],
        default=0,
        action="store",
        help="The rotation of the screen buffer in degrees. Default: 0",
    )
    cmdline_args_parser.add_argument(
        "--height",
        type=int,
        choices=[64],
        default=64,
        action="store",
        help="The pixel height of the screen buffer. Default: 64",
    )
    cmdline_args_parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        action="store",
        help="RaSCSI host. Default: localhost",
    )
    cmdline_args_parser.add_argument(
        "--port",
        type=int,
        default=6868,
        action="store",
        help="RaSCSI port. Default: 6868",
    )
    cmdline_args_parser.add_argument(
        "--password",
        type=str,
        default="",
        action="store",
        help="Token password string for authenticating with RaSCSI",
    )
    args = cmdline_args_parser.parse_args()
    config.ROTATION = args.rotation

    if args.height == 64:
        config.HEIGHT = 64
        config.LINES = 8
    elif args.height == 32:
        config.HEIGHT = 32
        config.LINES = 4
    config.TOKEN = args.password
    config.WIDTH = 128
    config.BORDER = 5
    config.RASCSI_HOST = args.host
    config.RASCSI_PORT = args.port

    return config


def main():
    config = parse_config()
    # print(config)

    ctrlboard_hw = CtrlBoardHardware()
    rascsi_client = RaScsiClient(SocketTools(), config.RASCSI_HOST, config.RASCSI_PORT)

    menu_renderer_config = MenuRendererConfig()
    menu_renderer_config.ssd1306_i2c_address = CtrlBoardHardwareConstants.SSD1306_I2C_ADDRESS
    menu_renderer_config.rotation = config.ROTATION

    menu_builder = CtrlBoardMenuBuilder(rascsi_client)
    menu_controller = MenuController(menu_builder=menu_builder, menu_renderer_config=menu_renderer_config)
    menu_controller.add(CtrlBoardMenuBuilder.SCSI_ID_MENU)
    menu_controller.add(CtrlBoardMenuBuilder.ACTION_MENU)

    menu_update_event_handler = CtrlBoardMenuUpdateEventHandler(menu_controller)
    ctrlboard_hw.attach(menu_update_event_handler)

    menu_controller.set_active_menu(CtrlBoardMenuBuilder.SCSI_ID_MENU)

    # menu_controller = MenuController(menu_renderer=menu_renderer)
    # print_event_handler = CtrlBoardPrintEventHandler()
    # ctrlboard_hw.attach(print_event_handler)

    while True:
        try:
            ctrlboard_hw.process_events()
            menu_controller.update()
        except KeyboardInterrupt:
            ctrlboard_hw.cleanup()
            break
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
