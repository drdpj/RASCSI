class MenuRendererConfig:
    width = 128
    height = 64
    ssd1306_i2c_address = 0x3c
#    font_path = 'resources/SourceCodePro-Bold.ttf'
    font_path = 'resources/DejaVuSansMono-Bold.ttf'
    font_size = 12
    row_selection_pixel_extension = 2
    scroll_behavior = "page"  # "extend" or "page"
#    scroll_behavior = "extend"  # "extend" or "page"
    transition = "PushTransition"
