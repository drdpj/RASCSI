from typing import Dict, Optional
from menu.menu import Menu
from menu.menu_builder import MenuBuilder
from menu.menu_renderer import MenuRenderer
from menu.menu_renderer_config import MenuRendererConfig
import importlib


class MenuController:

    def __init__(self, menu_builder: MenuBuilder, menu_renderer=None):
        self._menus: Dict[str, Menu] = {}
        self._active_menu: Optional[Menu] = None
        self._menu_renderer = menu_renderer
        self._menu_builder: MenuBuilder = menu_builder
        if self._menu_renderer is None:
            self._menu_renderer_config = MenuRendererConfig()
            self._menu_renderer = MenuRenderer(self._menu_renderer_config)
        self._transition = None
        try:
            module = importlib.import_module("menu.transition")
            try:
                transition_class = getattr(module, self._menu_renderer_config.transition)
                if transition_class is not None:
                    self._transition = transition_class(self._menu_renderer.disp)

            except AttributeError:
                print("transition [" + self._menu_renderer_config.transition + "] does not exist. Falling back to "
                                                                               "default.")
        except ImportError:
            print("transition module does not exist. Falling back to default.")
            self._transition = None

    def add(self, name: str, context_object=None):
        self._menus[name] = self._menu_builder.build(name)
        if context_object is not None:
            self._menus[name].context_object = context_object

    def set_active_menu(self, name: str):
        self._active_menu = self._menus[name]
        self._menu_renderer.set_menu(self._active_menu)
        self._menu_renderer.render()

    def refresh(self, name: str, context_object=None):
        item_selection = None
        if self._menus.get(name) is not None:
            item_selection = self._menus[name].item_selection
        self._menus[name] = self._menu_builder.build(name)

        if context_object is not None:
            self._menus[name].context_object = context_object

        if item_selection is not None:
            self._menus[name].item_selection = item_selection

    def get_active_menu(self):
        return self._active_menu

    def get_menu_renderer(self):
        return self._menu_renderer

    def get_rascsi_client(self):
        return self._menu_builder.get_rascsi_client()
