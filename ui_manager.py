# ui_manager.py
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from window_handler import open_chat_window, open_canvas_window
from popup_handler import PopupManager

from game_config import (
    WINDOWS_WIDTH, WINDOWS_HEIGHT, CHAT_ICON_ID, CANVAS_ICON_ID, ICON_CLASS_ID
)

class UIManager:
    def __init__(self, screen_resolution, theme_path):
        self.manager = pygame_gui.UIManager(screen_resolution, theme_path=theme_path)
        self.open_windows = [] # To keep track of currently open non-popup windows
        self.popup_manager = PopupManager(self.manager) # Manage pop-ups separately

        self._create_buttons()

    def _create_buttons(self):
        self.chat_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (40, 40)),
                                                        text='',
                                                        manager=self.manager,
                                                        object_id=ObjectID(object_id=CHAT_ICON_ID, class_id=ICON_CLASS_ID))

        self.canvas_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 275), (40, 40)),
                                                            text='',
                                                            manager=self.manager,
                                                            object_id=ObjectID(object_id=CANVAS_ICON_ID, class_id=ICON_CLASS_ID))

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_object_id.endswith("_icon"):
                self._handle_icon_button_press(event.ui_object_id)
            elif event.ui_element.text in ["Aceptar", "Dismiss"]: # Handle popup button presses
                self.popup_manager.handle_popup_button_press(event.ui_element, event.ui_element.text)
                return True # Indicate that a popup was handled

        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            self._handle_window_close(event.ui_element)

        self.manager.process_events(event)
        return False # Indicate no popup was handled

    def _handle_icon_button_press(self, object_id):
        icon_name = object_id.split("_")[0][1:]
        is_opened = any(w["window"].object_ids[0].split("_")[0][1:] == icon_name for w in self.open_windows)

        if not is_opened:
            if icon_name == "chat":
                self.open_windows.append(open_chat_window(self.manager))
            elif icon_name == "canvas":
                self.open_windows.append(open_canvas_window(self.manager))

    def _handle_window_close(self, closed_element):
        for w in self.open_windows:
            if w["window"].object_ids[0] == closed_element.object_ids[0]:
                self.open_windows.remove(w)
                break

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw(self, surface):
        self.manager.draw_ui(surface)