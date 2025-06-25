import pygame
import pygame_gui
import time
import random

from pygame_gui.core import ObjectID


class PopupManager:
    def __init__(self, manager, click_sound=None, error_sound=None):
        self.manager = manager
        self.click_sound = click_sound
        self.error_sound = error_sound
        self.active_popups = []
        self.last_popup_time = 0
        self.start_time = time.time()

        # Configuración de intervalos por minuto
        self.time_intervals = {
            1: [5, 10],  # Primer minuto: cada 5-10 segundos
            2: [3, 5],  # Segundo minuto: cada 3-5 segundos
            3: [0.5, 1.5]  # Tercer minuto: cada 0.5-1.5 segundos (se aloca todo)
        }

        # Contenidos hardcodeados para las ventanas
        self.popup_contents = [
            {
                "header": "¡Advertencia del Sistema!",
                "content": "Tu sistema ha detectado 47 virus.\n¿Deseas escanear ahora?"
            },
            {
                "header": "Actualización Crítica",
                "content": "Windows necesita reiniciarse\ninmediatamente para aplicar\nactualizaciones de seguridad."
            },
            {
                "header": "Error de Memoria",
                "content": "Memoria insuficiente.\nCierre algunas aplicaciones\npara continuar."
            },
            {
                "header": "¡Felicidades!",
                "content": "¡Eres el visitante número 1000!\nHaz clic aquí para reclamar\ntu premio de $1000!"
            },
            {
                "header": "Conexión Perdida",
                "content": "Se ha perdido la conexión\na Internet. Verificando...\nPor favor espere."
            },
            {
                "header": "Disco Lleno",
                "content": "El disco C: está lleno.\nElimina archivos innecesarios\no el sistema fallará."
            },
            {
                "header": "Firewall Desactivado",
                "content": "Tu firewall está desactivado.\nTu computadora está en riesgo.\n¡Actívalo ahora!"
            },
            {
                "header": "Registro Corrupto",
                "content": "El registro de Windows\nestá corrupto. Ejecuta\nla reparación automática."
            },
            {
                "header": "Spyware Detectado",
                "content": "Se ha detectado spyware\nen tu sistema. Ejecuta\nun análisis completo."
            },
            {
                "header": "Batería Baja",
                "content": "La batería está críticamente\nbaja. Conecta el cargador\ninmediatamente."
            }
        ]

    def get_current_minute(self):
        """Obtiene el minuto actual desde el inicio"""
        elapsed = time.time() - self.start_time
        return min(int(elapsed // 60) + 1, 3)  # Máximo 3 minutos

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
        """Crea una nueva ventana popup con contenido aleatorio"""

        # Seleccionar contenido aleatorio
        content = random.choice(self.popup_contents)

        # Posición aleatoria para la ventana
        window_width = 300
        window_height = 150
        max_x = self.manager.window_resolution[0] - window_width
        max_y = self.manager.window_resolution[1] - window_height

        x = random.randint(50, max(51, max_x))
        y = random.randint(50, max(51, max_y))

        # Crear la ventana
        window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(x, y, window_width, window_height),
            manager=self.manager,
            window_display_title=content["header"],
            object_id=ObjectID(class_id='#popup_window')
        )

        # Crear el texto del contenido
        text_area = pygame_gui.elements.UITextBox(
            html_text=content["content"],
            relative_rect=pygame.Rect(10, 10, window_width - 20, window_height - 80),
            manager=self.manager,
            container=window, #this is text_box in theme.json
        )

        # Crear botones
        ok_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, window_height - 60, 80, 30),
            text='OK',
            manager=self.manager,
            container=window
        )

        cancel_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(100, window_height - 60, 80, 30),
            text='Cancelar',
            manager=self.manager,
            container=window
        )

        # Reproducir sonido de error
        if self.error_sound:
            self.error_sound.play()

        # Crear componentes del popup
        popup_components = {
            "window": window,
            "text_area": text_area,
            "ok_button": ok_button,
            "cancel_button": cancel_button,
            "content": content
        }

        self.active_popups.append(popup_components)

        return popup_components

    def handle_popup_click(self, event):
        """Maneja los clics en los botones de los popups"""
        for popup in list(self.active_popups):
            if (event.ui_element == popup["ok_button"] or
                    event.ui_element == popup["cancel_button"]):

                if self.click_sound:
                    self.click_sound.play()

                popup["window"].kill()
                self.active_popups.remove(popup)
                return True
        return False

    def handle_popup_close(self, event):
        """Maneja cuando se cierra una ventana popup con la X"""
        for popup in list(self.active_popups):
            if event.ui_element == popup["window"]:
                self.active_popups.remove(popup)
                return True
        return False

    def update(self):
        """Actualiza el sistema de popups - debe llamarse en el loop principal"""
        # Verificar si es momento de crear un nuevo popup
        if self.should_create_popup():
            self.create_popup_window()

    def get_debug_info(self):
        """Información de debug para mostrar el estado actual"""
        current_minute = self.get_current_minute()
        interval = self.get_current_interval()
        active_count = len(self.active_popups)

        return {
            "minute": current_minute,
            "interval": interval,
            "active_popups": active_count,
            "elapsed_time": time.time() - self.start_time
        }

    def cleanup(self):
        """Limpia todos los popups activos"""
        for popup in self.active_popups:
            popup["window"].kill()
        self.active_popups.clear()