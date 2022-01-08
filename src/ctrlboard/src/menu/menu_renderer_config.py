class MenuRendererConfig:

    _rotation_mapper = {
        0: 0,
        90: 1,
        180: 2,
        270: 3
    }

    def __init__(self):
        self.width = 128
        self.height = 64
        self.ssd1306_i2c_address = 0x3c
        #    self.font_path = 'resources/SourceCodePro-Bold.ttf'
        self.font_path = 'resources/DejaVuSansMono-Bold.ttf'
        self.font_size = 12
        self.row_selection_pixel_extension = 2
        self.scroll_behavior = "page"  # "extend" or "page"
        #    self.croll_behavior = "extend"  # "extend" or "page"
        #    self.transition = "PushTransition"
        self.transition = "None"
        self.transition_attributes_left = {"direction": "push_left"}
        self.transition_attributes_right = {"direction": "push_right"}
        self.transition_speed = 20
        self.scroll_line = True
        self.scroll_delay = 3
        self.scroll_line_end_delay = 2
        self.screensaver_delay = 60
        self.rotation = 0  # degrees. Options: 0, 180

    def get_mapped_rotation(self):
        return self._rotation_mapper[self.rotation]


