from typing import List


class Menu:

    def __init__(self):
        self.entries: List = []
        self.item_selection = 0

    def add_entry(self, text, callback_function=None):
        entry = {"text": text, "callback": callback_function}
        self.entries.append(entry)

