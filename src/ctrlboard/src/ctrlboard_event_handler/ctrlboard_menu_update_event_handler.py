import time
import observer
from ctrlboard_hw.attributed_button import AttributedButton
from ctrlboard_hw.encoder import Encoder
from menu.menu_renderer import MenuRenderer


class CtrlBoardMenuUpdateEventHandler(MenuRenderer, observer.Observer):
    def update(self, updated_object):
        if isinstance(updated_object, AttributedButton):
            # print(updated_object.name + " has been pressed!")
            self.message = updated_object.name + " pressed!"
            self.render()
            time.sleep(1)
            self.message = ""
            self.render()
        if isinstance(updated_object, Encoder):
            # print(updatedObject.direction)
            if updated_object.direction == 1:
                self.menu.item_selection += 1
            if updated_object.direction == -1:
                self.menu.item_selection -= 1
            self.render()
