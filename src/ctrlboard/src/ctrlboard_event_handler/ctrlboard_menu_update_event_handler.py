import time
from menu.menu_renderer import MenuRenderer
from ctrlboard_hw.hardware_button import HardwareButton
from ctrlboard_hw.encoder import Encoder
from observer import Observer


class CtrlBoardMenuUpdateEventHandler(Observer):

    def __init__(self, menu_renderer: MenuRenderer):
        self.message = None
        self.menu_renderer = menu_renderer

    def update(self, updated_object):
        if isinstance(updated_object, HardwareButton):
            self.menu_renderer.message = updated_object.name + " pressed!"
            self.menu_renderer.render()
            time.sleep(1)
            self.menu_renderer.message = ""
            self.menu_renderer.render()
        if isinstance(updated_object, Encoder):
            # print(updatedObject.direction)
            if updated_object.direction == 1:
                self.menu_renderer.menu.item_selection += 1
            if updated_object.direction == -1:
                self.menu_renderer.menu.item_selection -= 1
            self.menu_renderer.render()
