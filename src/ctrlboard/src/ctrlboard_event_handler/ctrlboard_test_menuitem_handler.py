

class CtrlBoardTestMenuItemHandler:

    # noinspection PyMethodMayBeStatic
    def print_item_text_to_stdout(self, obj):
        if isinstance(obj, str):
            print(str(obj))
