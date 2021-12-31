import time
from menu.menu_renderer import MenuRenderer
from ctrlboard_hw.hardware_button import HardwareButton
from ctrlboard_hw.encoder import Encoder
from observer import Observer


class CtrlBoardMenuUpdateEventHandler(Observer):

    def __init__(self, menu_renderer: MenuRenderer, navigation_info):
        self.message = None
        self.menu_renderer = menu_renderer
        self.navigation_info = navigation_info

    def update(self, updated_object):
        if isinstance(updated_object, HardwareButton):
            if updated_object.name == "RotBtn":
                menu = self.menu_renderer.menu
                entry = dict(menu.entries[menu.item_selection])
                callback = entry["callback"]
                # print(entry['text'])
                # print(entry['callback'])
                if callback is not None:
                    if callback.__name__ == "transition_to_menu":
                        callback(self.menu_renderer, self.navigation_info["second_level_menu_renderer"])
                    elif callback.__name__ == "print_item_text_to_stdout":
                        callback(entry['text'])

            else:
                self.menu_renderer.message = updated_object.name + " pressed!"
                self.menu_renderer.render()
                time.sleep(1)
                self.menu_renderer.message = ""
                self.menu_renderer.render()
        if isinstance(updated_object, Encoder):
            # print(updatedObject.direction)
            if updated_object.direction == 1:
                if self.menu_renderer.menu.item_selection + 1 < len(self.menu_renderer.menu.entries):
                    self.menu_renderer.menu.item_selection += 1
            if updated_object.direction == -1:
                if self.menu_renderer.menu.item_selection - 1 >= 0:
                    self.menu_renderer.menu.item_selection -= 1
                else:
                    self.menu_renderer.menu.item_selection = 0
            self.menu_renderer.render()
