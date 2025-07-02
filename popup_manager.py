import pygame
import pygame_gui
import time
import random
import os.path
import json

import env_variables as e  # Assuming e.FIRST_STAGE_TIME and e.SECOND_STAGE_TIME are defined

from pygame_gui.core import ObjectID


class PopupManager:
    def __init__(self, manager, click_sound=None, error_sound=None,
                 gmail_sound=None, canvas_sound=None, whatsapp_sound=None,
                 windows_not1_sound=None, windows_not2_sound=None):
        self.manager = manager
        self.click_sound = click_sound
        self.error_sound = error_sound
        self.gmail_sound = gmail_sound
        self.canvas_sound = canvas_sound
        self.whatsapp_sound = whatsapp_sound
        self.windows_not1_sound = windows_not1_sound
        self.windows_not2_sound = windows_not2_sound
        self.active_popups = []
        self.last_popup_time = 0
        self.start_time = time.time()

        # Configuración de intervalos por minuto
        self.time_intervals = {
            1: [5, 10],  # Primer minuto
            2: [3, 5],  # Segundo minuto
            3: [0.8, 1.5]  # Tercer minuto
        }

        self.popup_types = ["canvas", "gmail", "whatsapp", "windows-notification", "windows-notification2"]
        self.popup_probabilities = [0.55, 0.1, 0.2, 0.1, 0.05]
        self.number_gmail_popup = 0
        self.number_whatsapp_popup = 0

        # --- Shutdown Button Attributes ---
        self.shutdown_button = None
        self.shutdown_button_timer = 0
        self.shutdown_button_visible_duration_stage1 = 5  # Visible for 5 seconds in stage 1
        self.shutdown_button_last_teleport_time = 0
        self.shutdown_button_teleport_interval_stage2 = [8, 12]  # Every 8-12 seconds
        self.shutdown_button_teleport_interval_stage3 = [2, 5]  # Every 2-5 seconds
        self.shutdown_button_on_screen_duration = 1.5  # Stays visible for 1.5s after teleport
        self.create_shutdown_button()

    def create_shutdown_button(self):
        """Creates the shutdown button, initially hidden."""
        button_width, button_height = 40, 40
        x = 0
        y = self.manager.window_resolution[1] - button_height
        self.shutdown_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(x, y, button_width, button_height),
            text='',
            manager=self.manager,
            object_id=ObjectID(class_id='#shutdown_button')
        )
        self.shutdown_button.hide()  # Start hidden

    def _teleport_shutdown_button(self):
        """Moves the shutdown button to a new random position and shows it."""
        if self.shutdown_button:
            button_width, button_height = self.shutdown_button.relative_rect.size
            max_x = self.manager.window_resolution[0] - button_width
            max_y = self.manager.window_resolution[1] - button_height
            new_x = random.randint(0, max_x)
            new_y = random.randint(0, max_y)
            self.shutdown_button.set_position(pygame.Vector2(new_x, new_y))
            self.shutdown_button.show()

    def get_current_minute(self):
        """Obtiene el minuto actual desde el inicio"""
        elapsed_seconds = time.time() - self.start_time

        if 0 <= elapsed_seconds < e.FIRST_STAGE_TIME:
            return 1
        elif elapsed_seconds < e.SECOND_STAGE_TIME:
            return 2
        else:
            return 3

    def get_current_interval(self):
        """Obtiene el intervalo actual basado en el minuto"""
        current_minute = self.get_current_minute()
        return self.time_intervals.get(current_minute, [0.5, 1.5])

    def should_create_popup(self):
        """Determina si es momento de crear una nueva ventana popup"""
        current_time = time.time()

        if (current_time - self.start_time < 6):
            return False
        interval_range = self.get_current_interval()

        if self.last_popup_time == 0:
            self.last_popup_time = current_time
            return True

        elapsed_since_last = current_time - self.last_popup_time
        next_popup_time = random.uniform(interval_range[0], interval_range[1])

        if elapsed_since_last >= next_popup_time:
            self.last_popup_time = current_time
            return True

        return False

    def open_file(self, filename):
        if (not os.path.isfile(filename)):
            print("No file exists", filename)
            return [{"header": "Error", "content": "File not found."}]

        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data

    def create_popup_window(self):
        category = random.choices(self.popup_types, weights=self.popup_probabilities, k=1)[0]
        filename = f"mensajes/notifications/{category}.json"
        filename_64 = f"mensajes/notifications_base64/{category}.json"

        current_minute = self.get_current_minute()
        content = {}

        # Simplified content loading
        use_base64 = False
        if current_minute == 2:
            use_base64 = random.random() < 0.1
        elif current_minute == 3:
            use_base64 = random.random() < 0.7

        chosen_file = filename_64 if use_base64 else filename
        content = random.choice(self.open_file(chosen_file))

        if category == "whatsapp":
            return self._create_whatsapp_popup(content)
        elif category == "gmail":
            return self._create_gmail_popup(content)
        elif category == "canvas":
            return self._create_canvas_popup(content)
        elif category == "windows-notification":
            return self._create_windows_popup(content)
        elif category == "windows-notification2":
            return self._create_windows_info_popup(content)

    def _create_whatsapp_popup(self, content):

        if self.whatsapp_sound:
            self.whatsapp_sound.play()

        window_width, window_height = 400, 150
        x = self.manager.window_resolution[0] - window_width - 20
        y = self.manager.window_resolution[1] - (window_height + 15) * (self.number_whatsapp_popup + 1) - 30

        self.number_whatsapp_popup = (self.number_whatsapp_popup + 1) % 4

        window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(x, y, window_width, window_height),
            manager=self.manager,
            window_display_title=content["header"],
            object_id=ObjectID(class_id='#whatsapp_window'),
        )
        main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, window_width, window_height),
            manager=self.manager,
            container=window,
            object_id=ObjectID(class_id='#error_main_panel')
        )

        text_area = pygame_gui.elements.UILabel(
            text=content["content"],
            relative_rect=pygame.Rect(0, -35, window_width, window_height - 10),
            manager=self.manager,
            container=main_panel,
            object_id=ObjectID(class_id='#error_text')
        )

        input_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(10, 60, window_width - 110, 30),
            manager=self.manager,
            container=main_panel,
            object_id=ObjectID(class_id='#error_input_button')
        )

        send_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(window_width - 90, 60, 80, 30),
            text="Enviar",
            manager=self.manager,
            container=main_panel,
            object_id=ObjectID(class_id='#error_ok_button')
        )

        self.active_popups.append({
            "window": window,
            "text_area": text_area,
            "input_box": input_box,
            "send_button": send_button,
            "content": content,
            "type": "whatsapp"
        })
        return window

    def _create_gmail_popup(self, content):
        if self.gmail_sound:
            self.gmail_sound.play()

        window_width, window_height = 350, 100
        x = 20
        y = self.manager.window_resolution[1] - (window_height + 15) * (self.number_gmail_popup + 1) - 30
        self.number_gmail_popup = (self.number_gmail_popup + 1) % 5

        window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(x, y, window_width, window_height),
            manager=self.manager,
            window_display_title=content["header"],
            object_id=ObjectID(class_id='#error_window'),
            resizable=False
        )
        main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, window_width, window_height),
            manager=self.manager,
            container=window,
            object_id=ObjectID(class_id='#error_main_panel')
        )
        text_area = pygame_gui.elements.UITextBox(
            html_text=content["content"],
            relative_rect=pygame.Rect(10, 10, window_width - 20, 50),
            manager=self.manager,
            container=main_panel,
            object_id=ObjectID(class_id='#error_text')
        )

        self.active_popups.append({
            "window": window,
            "text_area": text_area,
            "content": content,
            "type": "gmail"
        })
        return window

    def _create_canvas_popup(self, content):
        if self.canvas_sound:
            self.canvas_sound.play()

        window_width, window_height = 350, 100
        x = random.randint(50, self.manager.window_resolution[0] - window_width - 50)
        y = random.randint(50, self.manager.window_resolution[1] - window_height - 50)

        window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(x, y, window_width, window_height),
            manager=self.manager,
            window_display_title=content["header"],
            object_id=ObjectID(class_id='#error_window'),
            resizable=False
        )
        main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, window_width, window_height),
            manager=self.manager,
            container=window,
            object_id=ObjectID(class_id='#error_main_panel')
        )

        text_area = pygame_gui.elements.UITextBox(
            html_text=content["content"],
            relative_rect=pygame.Rect(10, 10, window_width - 20, 50),
            manager=self.manager,
            object_id=ObjectID(class_id='#error_text'),
            container=main_panel
        )

        self.active_popups.append({
            "window": window,
            "text_area": text_area,
            "content": content,
            "type": "canvas"
        })
        return window

    def _create_windows_popup(self, content):
        if self.windows_not1_sound:
            self.windows_not1_sound.play()

        window_width, window_height = 300, 150
        x = random.randint(50, self.manager.window_resolution[0] - window_width - 50)
        y = random.randint(50, self.manager.window_resolution[1] - window_height - 50)

        window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(x, y, window_width, window_height),
            manager=self.manager,
            window_display_title=content["header"],
            object_id="#error_window"
        )
        main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, window_width, window_height),
            manager=self.manager,
            container=window,
            object_id=ObjectID(class_id='#error_main_panel')
        )
        text_area = pygame_gui.elements.UITextBox(
            html_text=content["content"],
            relative_rect=pygame.Rect(10, 10, window_width - 20, 60),
            manager=self.manager,
            container=main_panel,
            object_id=ObjectID(class_id='#error_text')
        )

        ok_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, window_height - 60, 80, 30),
            text='OK',
            manager=self.manager,
            container=main_panel,
            object_id=ObjectID(class_id='#error_ok_button')
        )

        self.active_popups.append({
            "window": window,
            "text_area": text_area,
            "ok_button": ok_button,
            "content": content,
            "type": "windows"
        })
        return window

    def _create_windows_info_popup(self, content):
        if self.windows_not2_sound:
            self.windows_not2_sound.play()

        window_width, window_height = 350, 100
        x = self.manager.window_resolution[0] - window_width - 20
        y = self.manager.window_resolution[1] - window_height - 260

        window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(x, y, window_width, window_height),
            manager=self.manager,
            window_display_title=content["header"],
            object_id="#error_window",
            resizable=False
        )
        main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, window_width, window_height),
            manager=self.manager,
            container=window,
            object_id=ObjectID(class_id='#error_main_panel')
        )

        text_area = pygame_gui.elements.UITextBox(
            html_text=content["content"],
            relative_rect=pygame.Rect(10, 10, window_width - 20, 50),
            manager=self.manager,
            container=main_panel,
            object_id=ObjectID(class_id='#error_text')
        )

        self.active_popups.append({
            "window": window,
            "text_area": text_area,
            "content": content,
            "type": "windows_info"
        })
        return window

    def handle_popup_click(self, event):
        # --- Handle Shutdown Button Click ---
        if event.ui_element == self.shutdown_button:
            print("Shutdown button clicked!")
            # Add your game shutdown logic here
            # For example: pygame.event.post(pygame.event.Event(pygame.QUIT))
            return True

        for popup in list(self.active_popups):
            if event.ui_element in [popup.get("ok_button"), popup.get("cancel_button"), popup.get("send_button")]:
                if self.click_sound:
                    self.click_sound.play()
                popup["window"].kill()
                self.active_popups.remove(popup)
                return True
        return False

    def handle_popup_close(self, event):
        for popup in list(self.active_popups):
            if event.ui_element == popup["window"]:
                self.active_popups.remove(popup)
                return True
        return False

    def update(self):
        # Create popups based on timing
        if self.should_create_popup():
            self.create_popup_window()

        # --- Shutdown Button Logic ---
        current_time = time.time()
        current_stage = self.get_current_minute()

        # Stage 1: Appear for a few seconds, then disappear
        if current_stage == 1:
            # Show button at the start for the specified duration
            if not self.shutdown_button.visible and (
                    current_time - self.start_time) < self.shutdown_button_visible_duration_stage1:
                self.shutdown_button.show()
            # Hide it after the duration has passed
            elif self.shutdown_button.visible and (
                    current_time - self.start_time) >= self.shutdown_button_visible_duration_stage1:
                self.shutdown_button.hide()

        # Stages 2 & 3: Teleporting behavior
        elif current_stage in [2, 3]:
            # Determine teleport interval based on stage
            interval_range = self.shutdown_button_teleport_interval_stage2 if current_stage == 2 else self.shutdown_button_teleport_interval_stage3

            # Check if it's time to teleport the button
            next_teleport_time = random.uniform(interval_range[0], interval_range[1])
            if current_time - self.shutdown_button_last_teleport_time > next_teleport_time:
                self._teleport_shutdown_button()
                self.shutdown_button_last_teleport_time = current_time
                self.shutdown_button_timer = current_time

            # Check if the button has been on screen long enough to disappear
            if self.shutdown_button.visible and (
                    current_time - self.shutdown_button_timer) > self.shutdown_button_on_screen_duration:
                self.shutdown_button.hide()

    def cleanup(self):
        for popup in self.active_popups:
            popup["window"].kill()
        self.active_popups.clear()

        # --- Cleanup Shutdown Button ---
        if self.shutdown_button:
            self.shutdown_button.kill()

    def get_debug_info(self):
        return {
            "minute": self.get_current_minute(),
            "interval": self.get_current_interval(),
            "active_popups": len(self.active_popups),
            "elapsed_time": time.time() - self.start_time
        }