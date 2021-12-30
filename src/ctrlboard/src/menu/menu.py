from typing import List


class Menu:
    entries: List = []
    item_selection = 0

    def add_entry(self, text):
        self.entries.append(text)
