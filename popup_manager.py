import pygame
import pygame_gui
import time
import random
import env_variables as e
import numpy as np
import os.path
import json

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
            1: [5, 10],  # Primer minuto: cada 5-10 segundos
            2: [3, 5],  # Segundo minuto: cada 3-5 segundos
            3: [0.8, 1.5]  # Tercer minuto: cada 0.5-1.5 segundos (se aloca todo)
        }

        # Contenidos hardcodeados para las ventanas
        self.popup_types = ["canvas", "gmail", "whatsapp", "windows-notification", "windows-notification2"]
        self.popup_probabilities = [0.05, 0.05, 0.1, 0.6, 0.2]

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
        interval_range = self.get_current_interval()

        # Calcular el siguiente tiempo de popup basado en el rango
        if self.last_popup_time == 0:
            self.last_popup_time = current_time
            return True

        elapsed_since_last = current_time - self.last_popup_time
        next_popup_time = random.uniform(interval_range[0], interval_range[1])

        if elapsed_since_last >= next_popup_time:
            self.last_popup_time = current_time
            return True

        return False

    def create_popup_window(self):
        category = random.choices(self.popup_types, weights=self.popup_probabilities, k = 1)[0]
        filename = f"mensajes/notifications/{category}.json"
        print(category)
        if(not os.path.isfile(filename)):
            print("No file exists", filename)

        with open(filename, 'r') as file:
            data = json.load(file)

        content = random.choice(data)

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
        y = self.manager.window_resolution[1] - window_height - 20

        window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(x, y, window_width, window_height),
            manager=self.manager,
            window_display_title=content["header"],
            object_id="#popup_window",
            resizable=False
        )

        text_area = pygame_gui.elements.UITextBox(
            html_text=content["content"],
            relative_rect=pygame.Rect(10, 10, window_width - 20, 40),
            manager=self.manager,
            container=window
        )

        input_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(10, 60, window_width - 110, 30),
            manager=self.manager,
            container=window
        )

        send_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(window_width - 90, 60, 80, 30),
            text="Enviar",
            manager=self.manager,
            container=window
        )

        self.active_popups.append({
            "window": window,
            "text_area": text_area,
            "input_box": input_box,
            "send_button": send_button,
            "content": content
        })
        return window

    def _create_gmail_popup(self, content):

        if self.gmail_sound:
            self.gmail_sound.play()

        window_width, window_height = 350, 100
        x = self.manager.window_resolution[0] - window_width - 20
        y = self.manager.window_resolution[1] - window_height - 20

        window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(x, y, window_width, window_height),
            manager=self.manager,
            window_display_title=content["header"],
            object_id="#popup_window",
            resizable=False
        )

        text_area = pygame_gui.elements.UITextBox(
            html_text=content["content"],
            relative_rect=pygame.Rect(10, 10, window_width - 20, 50),
            manager=self.manager,
            container=window
        )

        self.active_popups.append({
            "window": window,
            "text_area": text_area,
            "content": content
        })
        return window

    def _create_canvas_popup(self, content):

        if self.canvas_sound:
            self.canvas_sound.play()

        window_width, window_height = 350, 100
        x = self.manager.window_resolution[0] - window_width - 20
        y = self.manager.window_resolution[1] - window_height - 140

        window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(x, y, window_width, window_height),
            manager=self.manager,
            window_display_title=content["header"],
            object_id="#popup_window",
            resizable=False
        )

        text_area = pygame_gui.elements.UITextBox(
            html_text=content["content"],
            relative_rect=pygame.Rect(10, 10, window_width - 20, 50),
            manager=self.manager,
            container=window
        )

        self.active_popups.append({
            "window": window,
            "text_area": text_area,
            "content": content
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
            object_id="#popup_window"
        )

        text_area = pygame_gui.elements.UITextBox(
            html_text=content["content"],
            relative_rect=pygame.Rect(10, 10, window_width - 20, 60),
            manager=self.manager,
            container=window
        )

        ok_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, window_height - 60, 80, 30),
            text='OK',
            manager=self.manager,
            container=window
        )

        self.active_popups.append({
            "window": window,
            "text_area": text_area,
            "ok_button": ok_button,
            "content": content
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
            object_id="#popup_window",
            resizable=False
        )

        text_area = pygame_gui.elements.UITextBox(
            html_text=content["content"],
            relative_rect=pygame.Rect(10, 10, window_width - 20, 50),
            manager=self.manager,
            container=window
        )

        self.active_popups.append({
            "window": window,
            "text_area": text_area,
            "content": content
        })
        return window

    def handle_popup_click(self, event):
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
        if self.should_create_popup():
            self.create_popup_window()

    def cleanup(self):
        for popup in self.active_popups:
            popup["window"].kill()
        self.active_popups.clear()

    def get_debug_info(self):
        return {
            "minute": self.get_current_minute(),
            "interval": self.get_current_interval(),
            "active_popups": len(self.active_popups),
            "elapsed_time": time.time() - self.start_time
        }
