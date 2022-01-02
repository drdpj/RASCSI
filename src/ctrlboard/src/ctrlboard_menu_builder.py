from file_cmds import FileTools
from menu.menu import Menu
from menu.menu_builder import MenuBuilder
from rascsi_client import RaScsiClient


class CtrlBoardMenuBuilder(MenuBuilder):
    SCSI_ID_MENU = "scsi_id_menu"
    ACTION_MENU = "action_menu"
    IMAGES_MENU = "images_menu"
    PROFILES_MENU = "profiles_menu"

    ACTION_OPENACTIONMENU = "openactionmenu"
    ACTION_RETURN = "return"
    ACTION_SLOT_ATTACHINSERT = "slot_attachinsert"
    ACTION_SLOT_DETACHEJECT = "slot_detacheject"
    ACTION_SLOT_INFO = "slot_info"
    ACTION_SHUTDOWN = "shutdown"
    ACTION_LOADPROFILE = "loadprofile"
    ACTION_IMAGE_ATTACHINSERT = "image_attachinsert"

    def __init__(self, rascsi_client: RaScsiClient):
        super().__init__(rascsi_client)

    def build(self, name: str) -> Menu:
        if name == CtrlBoardMenuBuilder.SCSI_ID_MENU:
            return self.create_scsi_id_list_menu()
        elif name == CtrlBoardMenuBuilder.ACTION_MENU:
            return self.create_action_menu()
        elif name == CtrlBoardMenuBuilder.IMAGES_MENU:
            return self.create_images_menu()
        elif name == CtrlBoardMenuBuilder.PROFILES_MENU:
            return self.create_profiles_menu()
        else:
            print("Provided menu name [" + name + "] cannot be built!")

    def create_scsi_id_list_menu(self):
        devices = self._rascsi_client .list_devices()
        reserved_ids = self._rascsi_client .get_reserved_ids()

        devices_by_id = {}
        for device in devices["device_list"]:
            devices_by_id[int(device["id"])] = device

        menu = Menu(CtrlBoardMenuBuilder.SCSI_ID_MENU)

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
            if file == "":
                menu_str += "(empty)"
            else:
                menu_str += file
            if device_type != "":
                menu_str += " [" + device_type + "]"

            menu.add_entry(menu_str, {"context": self.SCSI_ID_MENU,
                                      "action": self.ACTION_OPENACTIONMENU,
                                      "scsi_id": scsi_id})

        return menu

    # noinspection PyMethodMayBeStatic
    def create_action_menu(self):
        menu = Menu(CtrlBoardMenuBuilder.ACTION_MENU)
        menu.add_entry("Return", {"context": self.ACTION_MENU, "action": self.ACTION_RETURN})
        menu.add_entry("Attach/Insert", {"context": self.ACTION_MENU, "action": self.ACTION_SLOT_ATTACHINSERT})
        menu.add_entry("Detach/Eject", {"context": self.ACTION_MENU, "action": self.ACTION_SLOT_DETACHEJECT})
        menu.add_entry("Info", {"context": self.ACTION_MENU, "action": self.ACTION_SLOT_INFO})
        menu.add_entry("Load Profile", {"context": self.ACTION_MENU, "action": self.ACTION_LOADPROFILE})
        menu.add_entry("Shutdown", {"context": self.ACTION_MENU, "action": self.ACTION_SHUTDOWN})
        return menu

    def create_images_menu(self):
        menu = Menu(CtrlBoardMenuBuilder.IMAGES_MENU)
        images_info = self._rascsi_client.get_image_files_info()
        menu.add_entry("Return", {"context": self.IMAGES_MENU, "action": self.ACTION_RETURN})
        images = images_info["image_files"]
        device_types = self.get_rascsi_client().get_device_types()
        for image in images:
            menu.add_entry(str(image.name) + " [" + str(device_types["device_types"][int(image.type)-1]) + "]",
                           {"context": self.IMAGES_MENU, "name": str(image.name),
                            "device_type": str(device_types["device_types"][int(image.type)-1]),
                            "action": self.ACTION_IMAGE_ATTACHINSERT})

        return menu

    def create_profiles_menu(self):
        menu = Menu(CtrlBoardMenuBuilder.PROFILES_MENU)
        menu.add_entry("Return", {"context": self.IMAGES_MENU, "action": self.ACTION_RETURN})
        file_tools = FileTools(rascsi_client=self._rascsi_client)
        config_files = file_tools.list_config_files()
        for config_file in config_files:
            menu.add_entry(str(config_file),
                           {"context": self.PROFILES_MENU, "name": str(config_file),
                            "action": self.ACTION_LOADPROFILE})

        return menu

