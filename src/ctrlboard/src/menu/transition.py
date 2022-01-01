from abc import ABC, abstractmethod
from PIL import Image
from PIL import ImageDraw


class Transition:

    def __init__(self, disp):
        self.disp = disp

    @abstractmethod
    def perform(self, start_image: Image, end_image: Image) -> None:
        pass


class PushTransition(Transition):

    def perform(self, start_image: Image, end_image: Image):
        transition_image = Image.new('1', (self.disp.width, self.disp.height))
        transition_draw = ImageDraw.Draw(transition_image)

        for x in range(0, 128, 28):
            transition_draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
            left_region = start_image.crop((x, 0, 128, 64))
            right_region = end_image.crop((0, 0, x, 64))
            transition_image.paste(left_region, (0, 0, 128-x, 64))
            transition_image.paste(right_region, (128-x, 0, 128, 64))
            self.disp.image(transition_image)
            self.disp.show()

        self.disp.image(end_image)
        self.disp.show()
