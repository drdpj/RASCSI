from ctrlboard_event_handler.ctrlboard_test_menuitem_handler import CtrlBoardTestMenuItemHandler
from ctrlboard_hw.ctrlboard_hw import CtrlBoardHardware
from ctrlboard_hw.ctrlboard_hw_constants import CtrlBoardHardwareConstants
from menu.menu import Menu
from ctrlboard_event_handler.ctrlboard_menu_update_event_handler import CtrlBoardMenuUpdateEventHandler
# from ctrlboard_event_handler.ctrlboard_print_event_handler import CtrlBoardPrintEventHandler
from menu.menu_renderer import MenuRenderer
from menu.menu_renderer_config import MenuRendererConfig
from rascsi_client import RaScsiClient
from socket_cmds import SocketTools


def create_scsi_id_list_menu(rascsi_client):
    menuhandler = CtrlBoardTestMenuItemHandler()
    devices = rascsi_client.list_devices()
    reserved_ids = rascsi_client.get_reserved_ids()

    devices_by_id = {}
    for device in devices["device_list"]:
        devices_by_id[int(device["id"])+1] = device

    menu = Menu()

    if reserved_ids["status"] is False:
        menu.add_entry("No scsi ids reserved")

    for scsi_id in range(1, 8):
        device = None
        if devices_by_id.get(scsi_id) is not None:
            device = devices_by_id[scsi_id]
        file = "-"
        device_type = ""

#        check_id = str(scsi_id)
        if str(scsi_id) in reserved_ids["ids"]:
            file = "[Reserved]"
        elif device is not None:
            file = str(device["file"])
            device_type = str(device["device_type"])

        menu_str = str(scsi_id) + ":"
        menu_str += file
        if device_type != "":
            menu_str += " [" + device_type + "]"

        menu.add_entry(menu_str, menuhandler.transition_to_menu)

    return menu


def create_action_menu():
    # menuhandler = CtrlBoardTestMenuItemHandler()
    menu2 = Menu()
    menu2.add_entry("Return")
    menu2.add_entry("Attach/Insert")
    menu2.add_entry("Detach/Eject")
    menu2.add_entry("Info")
    menu2.add_entry("Load Profile")
    menu2.add_entry("General: Shutdown")
    return menu2


def main():
    ctrlboard_hw = CtrlBoardHardware()
    rascsi_client = RaScsiClient(SocketTools(), '192.168.10.155', 6868)

    menu_renderer_config = MenuRendererConfig()
    menu_renderer_config.ssd1306_i2c_address = CtrlBoardHardwareConstants.SSD1306_I2C_ADDRESS

    first_level_menu = create_scsi_id_list_menu(rascsi_client)
    second_level_menu = create_action_menu()

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
