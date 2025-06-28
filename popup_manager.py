import pygame
import pygame_gui
import time
import random

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
            1: [5, 10],  # Primer minuto: cada 5-10 segundos
            2: [3, 5],  # Segundo minuto: cada 3-5 segundos
            3: [0.5, 1.5]  # Tercer minuto: cada 0.5-1.5 segundos (se aloca todo)
        }

        # Contenidos hardcodeados para las ventanas
        self.popup_contents = [
            # windows-notification (20)
            {"category": "windows-notification", "header": "¡Advertencia del Sistema!",
             "content": "Tu sistema ha detectado 47 virus.\n¿Deseas escanear ahora?"},
            {"category": "windows-notification", "header": "Actualización Crítica",
             "content": "Windows necesita reiniciarse\npara aplicar actualizaciones."},
            {"category": "windows-notification", "header": "Espacio en Disco Bajo",
             "content": "El espacio en disco está casi lleno. Libera espacio para mejorar el rendimiento."},
            {"category": "windows-notification", "header": "Problema de Registro",
             "content": "Se ha detectado un problema con el registro del sistema."},
            {"category": "windows-notification", "header": "Sistema Sobrecargado",
             "content": "El sistema está experimentando una carga elevada."},
            {"category": "windows-notification", "header": "Error de Controlador",
             "content": "Un controlador de dispositivo ha dejado de funcionar correctamente."},
            {"category": "windows-notification", "header": "Copia de Seguridad Pendiente",
             "content": "Tu última copia de seguridad fue hace más de una semana."},
            {"category": "windows-notification", "header": "Aplicación No Responde",
             "content": "La aplicación no responde. ¿Deseas cerrarla o esperar?"},
            {"category": "windows-notification", "header": "Memoria Insuficiente",
             "content": "La memoria RAM está casi agotada. Cierra algunos programas."},
            {"category": "windows-notification", "header": "Error de Disco Duro",
             "content": "Se ha detectado un error en el disco duro. Considera hacer una revisión."},
            {"category": "windows-notification", "header": "Nuevo Dispositivo",
             "content": "Se ha conectado un nuevo dispositivo USB."},
            {"category": "windows-notification", "header": "Pantalla Azul",
             "content": "El sistema se ha recuperado de un error grave."},
            {"category": "windows-notification", "header": "Actualización Disponible",
             "content": "Hay actualizaciones importantes listas para instalar."},
            {"category": "windows-notification", "header": "Activación de Windows",
             "content": "Activa Windows para seguir usando todas las funciones."},
            {"category": "windows-notification", "header": "Acceso Denegado",
             "content": "No tienes permisos para realizar esta acción."},
            {"category": "windows-notification", "header": "Configuración de Energía",
             "content": "Tu batería está en modo de ahorro de energía."},
            {"category": "windows-notification", "header": "Resolución Cambiada",
             "content": "La resolución de pantalla fue ajustada automáticamente."},
            {"category": "windows-notification", "header": "Instalación Fallida",
             "content": "No se pudo instalar la actualización del sistema."},
            {"category": "windows-notification", "header": "Modo Seguro",
             "content": "Tu sistema se inició en modo seguro."},
            {"category": "windows-notification", "header": "Error Crítico",
             "content": "Se ha producido un error crítico del sistema. Reinicia para continuar."},

            # windows-notification2 (20)
            {"category": "windows-notification2", "header": "Conexión Baja",
             "content": "Tu conexión a internet es inestable."},
            {"category": "windows-notification2", "header": "Red No Disponible",
             "content": "No se puede conectar a la red especificada."},
            {"category": "windows-notification2", "header": "Servidor No Responde",
             "content": "El servidor no responde. Verifica tu conexión."},
            {"category": "windows-notification2", "header": "IP Duplicada",
             "content": "Se detectó una IP duplicada en la red."},
            {"category": "windows-notification2", "header": "Firewall Desactivado",
             "content": "Tu firewall está desactivado."},
            {"category": "windows-notification2", "header": "Proxy Inaccesible",
             "content": "No se puede acceder al servidor proxy configurado."},
            {"category": "windows-notification2", "header": "Actualización de Red",
             "content": "Hay controladores de red actualizados disponibles."},
            {"category": "windows-notification2", "header": "Red Conectada",
             "content": "Te has conectado exitosamente a la red Wi-Fi."},
            {"category": "windows-notification2", "header": "Wi-Fi Desactivado",
             "content": "Tu adaptador Wi-Fi está desactivado."},
            {"category": "windows-notification2", "header": "Configuración DNS",
             "content": "Se ha modificado la configuración de DNS."},
            {"category": "windows-notification2", "header": "Corte de Red",
             "content": "Se ha perdido la conexión con el servidor."},
            {"category": "windows-notification2", "header": "VPN Activa",
             "content": "Estás conectado a través de una VPN."},
            {"category": "windows-notification2", "header": "Cable Desconectado",
             "content": "El cable de red ha sido desconectado."},
            {"category": "windows-notification2", "header": "Ping Fallido",
             "content": "No se puede hacer ping al destino."},
            {"category": "windows-notification2", "header": "Red Pública",
             "content": "Estás conectado a una red pública. Revisa tu seguridad."},
            {"category": "windows-notification2", "header": "Contraseña Incorrecta",
             "content": "No se pudo conectar. Contraseña de red incorrecta."},
            {"category": "windows-notification2", "header": "Actualización de Firewall",
             "content": "El firewall se ha actualizado exitosamente."},
            {"category": "windows-notification2", "header": "Reinicio de Red Requerido",
             "content": "Reinicia el sistema para aplicar los cambios de red."},
            {"category": "windows-notification2", "header": "Puerto Cerrado",
             "content": "Se ha detectado un puerto de red cerrado."},
            {"category": "windows-notification2", "header": "Ancho de Banda Limitado",
             "content": "Tu ancho de banda actual está limitado."},

            # gmail (20)
            {"category": "gmail", "header": "Correo Nuevo", "content": "Tienes un nuevo correo de Recursos Humanos."},
            {"category": "gmail", "header": "Recordatorio de Entrevista",
             "content": "Entrevista programada para el jueves a las 10:00 a.m."},
            {"category": "gmail", "header": "Nueva Oferta Laboral",
             "content": "Te han ofrecido un puesto como Analista de Datos."},
            {"category": "gmail", "header": "Tu factura está disponible", "content": "Revisa tu factura de este mes."},
            {"category": "gmail", "header": "Alerta de Seguridad",
             "content": "Inició sesión un nuevo dispositivo en tu cuenta."},
            {"category": "gmail", "header": "Recibo de Compra", "content": "Gracias por tu compra en Amazon."},
            {"category": "gmail", "header": "Reestablecimiento de Contraseña",
             "content": "Haz clic aquí para reestablecer tu contraseña."},
            {"category": "gmail", "header": "Invitación a Calendario",
             "content": "Estás invitado a una reunión de equipo a las 15:00."},
            {"category": "gmail", "header": "Vacaciones Aprobadas",
             "content": "Tus vacaciones han sido confirmadas del 5 al 10 de julio."},
            {"category": "gmail", "header": "Nuevo Acceso Detectado",
             "content": "Hubo un intento de acceso desde Lima, Perú."},
            {"category": "gmail", "header": "Newsletter Junio", "content": "Descubre lo nuevo en tecnología este mes."},
            {"category": "gmail", "header": "Correo del Soporte Técnico",
             "content": "Tu ticket ha sido atendido, revisa la solución."},
            {"category": "gmail", "header": "Sorteo Ganado",
             "content": "¡Felicidades! Has ganado una gift card de $50."},
            {"category": "gmail", "header": "Cambios en Términos y Condiciones",
             "content": "Se han actualizado nuestras políticas de privacidad."},
            {"category": "gmail", "header": "Felicitaciones",
             "content": "Felicidades por completar el curso de Python."},
            {"category": "gmail", "header": "Informe Mensual",
             "content": "Aquí tienes el resumen mensual de tu cuenta."},
            {"category": "gmail", "header": "Participa en nuestra encuesta",
             "content": "Tu opinión es importante para nosotros."},
            {"category": "gmail", "header": "Actualización de Software",
             "content": "Descarga la nueva versión de nuestra app."},
            {"category": "gmail", "header": "Error de Entrega",
             "content": "No se pudo entregar tu mensaje a contacto@example.com."},
            {"category": "gmail", "header": "Suscripción Expirada",
             "content": "Tu suscripción ha expirado. Renuévala aquí."},

            # whatsapp (20) — solo mensajes directos, header = nombre
            {"category": "whatsapp", "header": "Juan", "content": "¿Ya terminaste la tarea de redes?"},
            {"category": "whatsapp", "header": "María", "content": "Nos vemos en la cafetería a las 5."},
            {"category": "whatsapp", "header": "Ana", "content": "Te llamé hace un rato, avísame cuando puedas."},
            {"category": "whatsapp", "header": "Pedro", "content": "Mira este sticker jajaja 😂"},
            {"category": "whatsapp", "header": "Camila", "content": "Te envié el audio con las instrucciones."},
            {"category": "whatsapp", "header": "Alejandro", "content": "¿Tienes el archivo del laboratorio 3?"},
            {"category": "whatsapp", "header": "Sofía", "content": "¡Hoy es mi cumple, no faltes al almuerzo!"},
            {"category": "whatsapp", "header": "Martín", "content": "¿Vamos al gimnasio después de clases?"},
            {"category": "whatsapp", "header": "Daniel", "content": "Revisa este video, es buenísimo."},
            {"category": "whatsapp", "header": "Sara", "content": "Este es el link que te dije: https://..."},
            {"category": "whatsapp", "header": "Lucía", "content": "¿Te gustó mi nueva foto de perfil?"},
            {"category": "whatsapp", "header": "Andrés", "content": "Estoy en camino, llego en 10 min."},
            {"category": "whatsapp", "header": "Valeria", "content": "¿Revisaste el informe que mandé?"},
            {"category": "whatsapp", "header": "Diego", "content": "Necesito ayuda con el código del proyecto."},
            {"category": "whatsapp", "header": "Paula", "content": "Hola! ¿Tienes las diapositivas de la clase?"},
            {"category": "whatsapp", "header": "Rodrigo", "content": "¿Al final sí habrá quiz hoy?"},
            {"category": "whatsapp", "header": "Elena", "content": "Gracias por prestarme el libro 😊"},
            {"category": "whatsapp", "header": "Luis", "content": "¿Podemos reunirnos a repasar hoy?"},
            {"category": "whatsapp", "header": "Carla", "content": "No entiendo la pregunta 3 del parcial."},
            {"category": "whatsapp", "header": "Renato", "content": "Te compartí mi ubicación, estoy aquí."},

            # canvas (20)
            {"category": "canvas", "header": "Prof. Gonzalo Castillo",
             "content": "Subí los apuntes para la clase de redes."},
            {"category": "canvas", "header": "Prof. Alejandra Reyes",
             "content": "La evaluación del proyecto ya está publicada."},
            {"category": "canvas", "header": "Prof. Rodrigo Torres",
             "content": "Recuerden entregar el laboratorio 4 antes del jueves."},
            {"category": "canvas", "header": "Prof. Mariana Pérez",
             "content": "Examen parcial este viernes a las 9:00 a.m."},
            {"category": "canvas", "header": "Prof. Luis Cárdenas", "content": "La clase de mañana será por Zoom."},
            {"category": "canvas", "header": "Prof. Andrea Valdez",
             "content": "Nueva actividad subida: 'Quiz de Capa de Red'."},
            {"category": "canvas", "header": "Prof. Juan Meza", "content": "Ya está habilitado el foro de dudas."},
            {"category": "canvas", "header": "Prof. Cecilia Álvarez",
             "content": "Se cambió la fecha de entrega del trabajo final."},
            {"category": "canvas", "header": "Prof. Martín Vargas",
             "content": "Les comparto la grabación de la clase."},
            {"category": "canvas", "header": "Prof. Elena Contreras",
             "content": "Revisen los comentarios sobre sus informes."},
            {"category": "canvas", "header": "Prof. Diego Herrera",
             "content": "Material complementario disponible en recursos."},
            {"category": "canvas", "header": "Prof. Paula Salinas",
             "content": "Encuesta sobre el curso activa hasta el domingo."},
            {"category": "canvas", "header": "Prof. Jorge Luján",
             "content": "Lectura obligatoria para el lunes: Cap. 6 y 7."},
            {"category": "canvas", "header": "Prof. Romina Fajardo",
             "content": "Están abiertas las inscripciones para la asesoría."},
            {"category": "canvas", "header": "Prof. Nicolás Ramírez",
             "content": "Trabajo grupal subido a la plataforma."},
            {"category": "canvas", "header": "Prof. Daniela Pino",
             "content": "No habrá clase mañana por actividad institucional."},
            {"category": "canvas", "header": "Prof. Ricardo Vásquez",
             "content": "Subí las soluciones del examen anterior."},
            {"category": "canvas", "header": "Prof. Camila Arévalo",
             "content": "Tienen hasta el viernes para entregar la práctica 5."},
            {"category": "canvas", "header": "Prof. Alberto Díaz",
             "content": "Ya pueden revisar sus notas del módulo 1."},
            {"category": "canvas", "header": "Prof. Silvia Montoya",
             "content": "Importante: revisen los horarios de recuperación."}
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
        content = random.choice(self.popup_contents)
        category = content["category"]

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
            object_id=ObjectID(class_id='#error_window')
        )
        main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, window_width, window_height),
            manager=self.manager,
            container=window,
            object_id=ObjectID(class_id='#error_main_panel') #reusing class
        )

        # Crear el texto del contenido
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
            object_id=ObjectID(class_id='#error_window'),
            resizable=False
        )
        main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, window_width, window_height),
            manager=self.manager,
            container=window,
            object_id=ObjectID(class_id='#error_main_panel')  # reusing class
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
            object_id=ObjectID(class_id='#error_window'),
            resizable=False
        )
        main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, window_width, window_height),
            manager=self.manager,
            container=window,
            object_id=ObjectID(class_id='#error_main_panel')  # reusing class
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
            object_id="#error_window"
        )
        main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, window_width, window_height),
            manager=self.manager,
            container=window,
            object_id=ObjectID(class_id='#error_main_panel')  # reusing class
        )
        text_area = pygame_gui.elements.UITextBox(
            html_text=content["content"],
            relative_rect=pygame.Rect(10, 10, window_width - 20, 60),
            manager=self.manager,
            container=x,
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
            object_id="#error_window",
            resizable=False
        )

        main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, window_width, window_height),
            manager=self.manager,
            container=window,
            object_id=ObjectID(class_id='#error_main_panel')  # reusing class
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
