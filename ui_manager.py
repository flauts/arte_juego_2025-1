# ui_manager.py
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from popup_handler import PopupManager # Import PopupManager

from game_config import (
    WINDOWS_WIDTH, WINDOWS_HEIGHT, CHAT_ICON_ID, CANVAS_ICON_ID, ICON_CLASS_ID
)

class UIManager:
    def __init__(self, screen_resolution, theme_path, game_state_ref):
        self.manager = pygame_gui.UIManager(screen_resolution, theme_path=theme_path)
        self.open_windows = [] # To keep track of currently open non-popup windows
        # Pass the main UIManager and GameState reference to the PopupManager
        self.popup_manager = PopupManager(self.manager, game_state_ref)

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
        """Processes a single Pygame event for the UI."""
        handled_by_popup = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            # Check if it's one of the main icon buttons
            if event.ui_object_id.endswith("_icon"):
                self._handle_icon_button_press(event.ui_object_id)
            # Check if it's a button within a popup window (by checking object_id class_id)
            elif "#popup_button" == str(event.ui_element.class_ids[1]):
                handled_by_popup = self.popup_manager.handle_popup_button_press(event.ui_element, event.ui_element.text)

        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            # Handle closing of main windows (popups are handled by PopupManager's internal logic)
            self._handle_window_close(event.ui_element)

        # Only process with the main UIManager if the event wasn't fully handled by a popup button
        if not handled_by_popup:
            self.manager.process_events(event)
        return handled_by_popup # Indicate if a popup was handled (might be useful for external logic)


    def _handle_icon_button_press(self, object_id):
        """Handles clicks on the main icon buttons (chat, canvas)."""
        icon_name = object_id.split("_")[0][1:]
        # Check if the window is already open
        is_opened = any(w['window'].object_ids[0].split("_")[0][1:] == icon_name for w in self.open_windows)

        if not is_opened:
            if icon_name == "chat":
                # Call the internal method to open the chat window
                self.open_windows.append(self._open_chat_window(self.manager))
            elif icon_name == "canvas":
                # Call the internal method to open the canvas window
                self.open_windows.append(self._open_canvas_window(self.manager))

    def _handle_window_close(self, closed_element):
        """Handles the closing of any UIWindow (excluding popups managed by PopupManager)."""
        # Iterate through currently open main windows and remove the closed one
        for w in self.open_windows:
            if w["window"].object_ids[0] == closed_element.object_ids[0]:
                self.open_windows.remove(w)
                break

    def update(self, time_delta):
        """Updates the Pygame GUI manager."""
        self.manager.update(time_delta)

    def draw(self, surface):
        """Draws all UI elements onto the given surface."""
        self.manager.draw_ui(surface)

    # --- Functions moved from original window_handler.py for main windows ---
    def _open_canvas_window(self, manager):
        """Creates and returns the canvas window."""
        canvas_window = pygame_gui.elements.UIWindow(rect=pygame.Rect((100, 100), (400, 400)),manager=manager,
                                                 window_display_title='Canvas',draggable=True,
                                                     object_id=ObjectID(object_id='@canvas_window',
                                                                        class_id="#window"))

        canvas_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((10, 30), (380, 360)),
            manager=manager,
            container=canvas_window
        )
        return {
            "window": canvas_window,
        }


    def _open_chat_window(self, manager):
        """Creates and returns the chat window along with its sub-elements."""
        # Create the main chat window
        chat_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((100, 100), (450, 500)),
            manager=manager,
            window_display_title='Chat Room',
            draggable=True,
            object_id=ObjectID(object_id='@chat_window', class_id="#window")
        )

        # Create main panel inside the window
        main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((5, 30), (440, 465)),
            manager=manager,
            container=chat_window
        )

        # Chat display area (scrollable text box for messages)
        chat_display = pygame_gui.elements.UITextBox(
            html_text="<b>Welcome to the chat!</b><br>"
                      "System: Chat room initialized<br>"
                      "<font color='#0066CC'>User1:</font> Hello everyone!<br>"
                      "<font color='#CC6600'>User2:</font> Hey there!<br>",
            relative_rect=pygame.Rect((10, 10), (420, 350)),
            manager=manager,
            container=main_panel
        )

        # Input field for typing messages
        message_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 370), (320, 30)),
            manager=manager,
            container=main_panel,
            placeholder_text="Type your message here..."
        )

        # Send button
        send_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((340, 370), (80, 30)),
            text='Send',
            manager=manager,
            container=main_panel
        )

        # Online users list (optional)
        users_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 410), (100, 20)),
            text='Online Users:',
            manager=manager,
            container=main_panel
        )

        users_list = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((120, 410), (150, 45)),
            item_list=['User1', 'User2', 'User3'],
            manager=manager,
            container=main_panel
        )

        # Clear chat button
        clear_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((280, 410), (80, 25)),
            text='Clear',
            manager=manager,
            container=main_panel
        )

        # Settings button
        settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((280, 435), (80, 20)),
            text='Settings',
            manager=manager,
            container=main_panel
        )

        return {
            'window': chat_window,
            'chat_display': chat_display,
            'message_input': message_input,
            'send_button': send_button,
            'users_list': users_list,
            'clear_button': clear_button,
            'settings_button': settings_button
        }