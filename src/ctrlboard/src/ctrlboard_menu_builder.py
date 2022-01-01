from menu.menu import Menu
from menu.menu_builder import MenuBuilder
from rascsi_client import RaScsiClient


class CtrlBoardMenuBuilder(MenuBuilder):

    _SCSI_ID_MENU = "scsi_id_menu"
    _ACTION_MENU = "action_menu"

    def __init__(self, rascsi_client: RaScsiClient):
        self._rascsi_client = rascsi_client

    def build(self, name: str):
        if name == CtrlBoardMenuBuilder._SCSI_ID_MENU:
            return self.create_scsi_id_list_menu()
        elif name == CtrlBoardMenuBuilder._ACTION_MENU:
            return self.create_action_menu()
        else:
            print("Provided menu name [" + name + "] cannot be built!")

    def create_scsi_id_list_menu(self):
        devices = self._rascsi_client .list_devices()
        reserved_ids = self._rascsi_client .get_reserved_ids()

        devices_by_id = {}
        for device in devices["device_list"]:
            devices_by_id[int(device["id"])] = device

        menu = Menu(CtrlBoardMenuBuilder._SCSI_ID_MENU)

        if reserved_ids["status"] is False:
            menu.add_entry("No scsi ids reserved")

        for scsi_id in range(0, 8):
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

            menu.add_entry(menu_str, {"context": "scsi_id_list_menu",
                                      "action": "open_action_menu",
                                      "scsi_id": scsi_id})

        return menu

    # noinspection PyMethodMayBeStatic
    def create_action_menu(self):
        menu = Menu(CtrlBoardMenuBuilder._ACTION_MENU)
        menu.add_entry("Return", {"context": "action_menu", "action": "return"})
        menu.add_entry("Attach/Insert", {"context": "action_menu", "action": "slot_command_attach_insert"})
        menu.add_entry("Detach/Eject", {"context": "action_menu", "action": "slot_command_detach_eject"})
        menu.add_entry("Info", {"context": "action_menu", "action": "slot_command_info"})
        menu.add_entry("Load Profile", {"context": "action_menu", "action": "load_profile"})
        menu.add_entry("General: Shutdown", {"context": "action_menu", "action": "shutdown"})
        return menu
