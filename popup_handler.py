# popup_handler.py
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.windows import UIMessageWindow
import json
import random

import game_config

POPUP_DATA_FILE = "popups.json" # Renamed for clarity

class PopupManager:
    def __init__(self, ui_manager, game_state_ref):
        self.ui_manager = ui_manager
        self.game_state = game_state_ref # Reference to the GameState object
        self.active_popups = [] # Stores dictionary for active popups: {'window': UIMessageWindow, 'data': popup_data}

        # Load all popup data at initialization
        try:
            with open(POPUP_DATA_FILE, "r", encoding="utf-8") as f:
                self.all_popup_data = json.load(f)
        except FileNotFoundError:
            print(f"Error: {POPUP_DATA_FILE} not found. Popups will not be available.")
            self.all_popup_data = {}

    def create_popup_for_stage(self, stage, screen_size=(800, 600)):
        """
        Creates and returns a new popup window based on the current stage.
        Returns None if no suitable popup is found or max popups are active.
        """
        stage_key = f"stage_{stage}"
        if stage_key not in self.all_popup_data:
            return None # No popups defined for this stage

        available_popups_for_stage = self.all_popup_data.get(stage_key, [])
        if not available_popups_for_stage:
            return None # No popups available in this stage

        if stage == 1:
            if len(self.active_popups) >= game_config.MAX_POP_UPS_STAGE_ONE: # Limit active popups (from game_config.MAX_POP_UPS_STAGE_ONE)
                return None
        if stage == 2:
            if len(self.active_popups) >= game_config.MAX_POP_UPS_STAGE_TWO:
                return None
        if stage == 3:
            if len(self.active_popups) >= game_config.MAX_POP_UPS_STAGE_THREE:
                return None
        popup_data = random.choice(available_popups_for_stage)

        new_popup_window = self._create_message_window(popup_data, screen_size)
        popup_info = {'window': new_popup_window, 'data': popup_data}
        self.active_popups.append(popup_info)
        return popup_info

    def _create_message_window(self, popup_data, screen_size, window_size=(300, 150)):
        """Private helper to create the actual UIMessageWindow from popup_data."""
        max_x = screen_size[0] - window_size[0]
        max_y = screen_size[1] - window_size[1]
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)

        rect = pygame.Rect((x, y), window_size)

        title = popup_data.get("title", "Mensaje")
        message = "<font face='retro'>" + popup_data.get("message", "") + "</font>"
        message_window = pygame_gui.elements.UIWindow(
                rect=rect,
                manager=self.ui_manager,
                window_display_title=title,
                object_id=ObjectID(class_id='#message_window',object_id=f"@message_window_{popup_data['id']}"),
                visible=False # Initially hidden, will be shown explicitly later
            )

        text = pygame_gui.elements.UITextBox(
            html_text=message,
            relative_rect=pygame.Rect((10, 10), (window_size[0] - 20, window_size[1] - 55)), # Adjusted height for buttons
            manager=self.ui_manager,
            container=message_window,
            object_id=ObjectID(class_id='#popup_text')
        )

        options = popup_data.get("options", [])
        num_options = len(options)
        if num_options == 0: # Handle case with no options
            return message_window

        button_width = (window_size[0] - 30) // num_options
        button_height = 25
        padding = 5
        total_button_width = num_options * button_width + (num_options - 1) * padding
        start_x = (window_size[0] - total_button_width) // 2
        y_pos = window_size[1] - button_height- 30 # Position buttons at the bottom

        for i, option in enumerate(options):
            button_rect = pygame.Rect(
                (start_x + i * (button_width + padding), y_pos),
                (button_width, button_height)
            )
            pygame_gui.elements.UIButton(
                relative_rect=button_rect,
                text=option["label"],
                manager=self.ui_manager,
                container=message_window,
                object_id=ObjectID(object_id=f"@popup_button_{popup_data['id']}_{option['label']}", class_id='#popup_button')
            )
        return message_window

    def handle_popup_button_press(self, ui_element, button_text):
        """
        Handles button presses within pop-up windows.
        Applies consequences to game state and potentially triggers follow-up popups.
        Returns True if a popup was handled, False otherwise.
        """
        # Find the parent window of the pressed button
        parent_window_id = ui_element.object_ids[0]
        corresponding_popup_info = None

        for popup in self.active_popups:
            if popup['window'].object_ids[0] == parent_window_id:
                corresponding_popup_info = popup
                break

        if corresponding_popup_info:
            popup_data = corresponding_popup_info['data']
            chosen_option = None
            for option in popup_data.get("options", []):
                if option["label"] == button_text:
                    chosen_option = option
                    break
            # Remove and kill the processed popup
            corresponding_popup_info['window'].kill()
            self.active_popups.remove(corresponding_popup_info)
            return True
        return False