import time

from menu.menu_renderer import MenuRenderer
from PIL import Image
from PIL import ImageDraw


class CtrlBoardTestMenuItemHandler:

    # noinspection PyMethodMayBeStatic
    def print_item_text_to_stdout(self, obj):
        if isinstance(obj, str):
            print(str(obj))

    # noinspection PyMethodMayBeStatic
    def transition_to_menu(self, first_menu_renderer: MenuRenderer, second_menu_renderer: MenuRenderer):
        disp = first_menu_renderer.disp
        first_menu_renderer.render(False)
        second_menu_renderer.render(False)
        first_image = first_menu_renderer.image
        second_image = second_menu_renderer.image

        transition_image = Image.new('1', (disp.width, disp.height))
        transition_draw = ImageDraw.Draw(transition_image)

        for x in range(0, 128, 18):
            transition_draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)
            left_region = first_image.crop((x, 0, 128, 64))
            right_region = second_image.crop((0, 0, x, 64))
            transition_image.paste(left_region, (0, 0, 128-x, 64))
            transition_image.paste(right_region, (128-x, 0, 128, 64))
            disp.image(transition_image)
            disp.show()

        disp.image(second_image)
        disp.show()

