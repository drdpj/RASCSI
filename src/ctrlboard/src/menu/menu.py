from typing import List


class Menu:
    entries: List = []
    item_selection = 0

    def add_entry(self, text, callback_function=None):
        entry = {"text": text, "callback": callback_function}
        self.entries.append(entry)
