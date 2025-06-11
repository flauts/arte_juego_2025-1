# popup_handler.py
import pygame_gui
from pygame_gui.windows import UIMessageWindow
import datetime
import json
POPUP_PATH = "popups2.json"

with open(POPUP_PATH, "r", encoding="utf-8") as f:
    POPUP_MESSAGES = json.load(f)
# --- End mock data ---


class PopupManager:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.active_popups = [] # Stores references to the UIWindow objects

    def create_popup_from_stage(self, stage, player_state):
        # This is a simplified version. In a real game, you'd have more complex logic
        # to determine which pop-up to show based on the stage, player state, and
        # whether specific pop-ups have already been shown/dismissed.

        # For demonstration, we'll just cycle through a few example messages.
        if stage == 1 and len(self.active_popups) < 2:
            # Example: pick a random message that hasn't been shown recently
            # or based on player_state
            message_data = POPUP_MESSAGES[len(self.active_popups) % len(POPUP_MESSAGES)]
            popup_window = self._create_message_window(message_data)
            self.active_popups.append(popup_window)
            return {"window": popup_window, "id": message_data["id"]} # Return the window and its ID for tracking
        return None # No popup to show

    def _create_message_window(self, message_data):
        # Create UIMessageWindow
        message_window = UIMessageWindow(
            html_message=message_data["message"],
            window_title=message_data["title"],
            manager=self.ui_manager,
            rect=pygame.Rect((200, 200), (400, 200)),
            object_id=f"@{message_data['id']}_popup_window" # Unique ID for the window
        )

        # Add buttons based on options
        button_width = 100
        button_height = 30
        x_offset = 20
        y_offset = message_window.get_relative_rect().height - button_height - 10

        for i, option in enumerate(message_data["options"]):
            button_rect = pygame.Rect(
                (message_window.get_relative_rect().width - button_width - x_offset - (button_width + x_offset) * i,
                 y_offset),
                (button_width, button_height)
            )
            pygame_gui.elements.UIButton(
                relative_rect=button_rect,
                text=option["label"],
                manager=self.ui_manager,
                container=message_window,
                object_id=f"@{message_data['id']}_popup_button_{option['label']}"
            )
        return message_window

    def handle_popup_button_press(self, ui_element, button_text):
        # Find which popup this button belongs to
        popup_window_id = ui_element.container.object_ids[0] # Get the parent window's object_id

        for popup in self.active_popups:
            if popup.object_ids[0] == popup_window_id:
                # Process consequence based on button_text (e.g., "Aceptar", "Dismiss")
                # This is where you would apply game state changes based on player choice
                # For now, we'll just close the popup.
                popup.kill()
                self.active_popups.remove(popup)
                return True
        return False # No popup handled