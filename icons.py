import pygame
import pygame_gui
import os
import random
import time
import env_variables as env

from pygame_gui.core import ObjectID

class IconGrid:
    def __init__(self, manager, window_width, window_height):
        self.manager = manager
        self.window_width = window_width
        self.window_height = window_height
        self.icons = []
        self.icon_width = 106
        self.icon_height = 170
        self.icon_size = 106
        self.grid_cols = 18
        self.grid_rows = 6
        self.start_x = 0
        self.start_y = 0
        self.icon_base_path = "ui_icons"
        self.start_time = time.time()
        self.weight_icon_screen = {
            1: 0.25,
            2: 0.5,
            3: 1
        }

        self.available_icons = [
            ("canvas.png", "Canvas"),
            ("whatsapp.png", "WhatsApp"),
            ("notepad.png", "Notepad"),
            ("call.png", "Call"),
            ("favorites.png", "Favorites"),
            ("fileexplorer.png", "FileExplorer"),
            ("7zip.png", "7Zip"),
            ("apps.png", "Apps"),
            ("audio.png", "Audio"),
            ("find.png", "Find"),
            ("lupa.png", "Lupa"),
            ("MediaPlayer.png", "MediaPlayer"),
            ("micnetframework.png", "MN Framework"),
            ("moviemaker.png", "MovieMaker"),
            ("mypc.png", "My PC"),
            ("networkconnections.png", "Connections"),
            ("p2p.png", "P2P"),
            ("people.png", "People"),
            ("pinball.png", "Pinball"),
            ("read.png", "Read"),
            ("sign.png", "Sign"),
            ("status.png", "Status"),
            ("storage.png", "Storage"),
            ("systemrestore.png", "System Restore"),
            ("terminal.png", "Terminal"),
            ("Transfer.png", "Transfer"),
            ("windowsexplorer.png", "Windows Explorer"),
            ("winrar.png", "WinRAR"),
            ("winzip.png", "WinZip"),
            ("wmplayer.png", "WMPlayer"),
            ("word.png", "Word"),
            ("zoom.png", "Zoom"),
            ("gmail.png", "Gmail"),
            #Para aqui empiezan las notepads
            ("notepad.png", "apuntes_algoritmos"),
            ("notepad.png", "tareas_matematica_discreta"),
            ("notepad.png", "resumen_redes"),
            ("notepad.png", "repaso_final_bd"),
            ("notepad.png", "ejercicios_lógica"),
            ("notepad.png", "proyecto_ia"),
            ("notepad.png", "quizs_historia"),
            ("notepad.png", "clase_etica"),
            ("notepad.png", "apuntes_circuitos"),
            ("notepad.png", "resumen_fisica"),
            ("notepad.png", "simulacro_parcial"),
            ("notepad.png", "preguntas_orales"),
            ("notepad.png", "notas_metodología"),
            ("notepad.png", "apuntes_tesis"),
            ("notepad.png", "pendientes_semanales"),
            ("notepad.png", "ideas_app"),
            ("notepad.png", "resumen_libro"),
            ("notepad.png", "glosario_sistemas"),
            ("notepad.png", "resumen_normas_apa"),
            ("notepad.png", "borrador_ensayo"),
            ("notepad.png", "tareas_prog2"),
            ("notepad.png", "lecturas_digitales"),
            ("notepad.png", "mapa_mental"),
            ("notepad.png", "listas_de_verificación"),
            ("notepad.png", "examen_pasado_compi"),
            ("notepad.png", "profe_comentarios"),
            ("notepad.png", "ensayo_filosofia"),
            ("notepad.png", "notas_reunión_grupo"),
            ("notepad.png", "resumen_clase_28_mayo"),
            ("notepad.png", "guias_de_laboratorio"),
            ("notepad.png", "preparación_sustitutorio"),
            ("notepad.png", "plan_estudio_junio"),
            ("notepad.png", "tareas_debidas"),
            ("notepad.png", "consultas_dudas"),
            ("notepad.png", "lectura_semana4"),
            ("notepad.png", "script_prueba_sql"),
            ("notepad.png", "errores_comunes_cpp"),
            ("notepad.png", "sintaxis_python"),
            ("notepad.png", "esquema_memo"),
            ("notepad.png", "pasos_para_instalar"),
            ("notepad.png", "código_fuente_demo"),
            ("notepad.png", "definiciones_clave"),
            ("notepad.png", "practica_logica"),
            ("notepad.png", "problemas_modelados"),
            ("notepad.png", "resumen_cpp_intermedio"),
            ("notepad.png", "tips_presentacion"),
            ("notepad.png", "casos_estudio"),
            ("notepad.png", "fechas_importantes"),
            ("notepad.png", "bitacora_progreso"),
            ("notepad.png", "metas_mensuales")

        ]

        self.check_available_icons()
        self.create_initial_icons()

    def check_available_icons(self):
        """Verificar qué iconos están realmente disponibles en disco"""
        available_icons = []
        missing_icons = []

        for icon_file, label in self.available_icons:
            icon_path = os.path.join(self.icon_base_path, icon_file)
            if os.path.exists(icon_path):
                available_icons.append((icon_file, label))
            else:
                missing_icons.append(icon_file)

        # Usar solo los iconos disponibles
        self.available_icons = available_icons


    def create_initial_icons(self):
        """Crear los iconos iniciales en el grid"""
        # Iconos fijos iniciales
        initial_positions = [
            (0, 0, "canvas.png", "Canvas"),
            (1, 0, "whatsapp.png", "WhatsApp"),
            (3, 0, "gmail.png", "Gmail"),
            (4, 0, "zoom.png", "Zoom")
        ]
        for col, row, icon_file, label in initial_positions:
            icon_path = os.path.join(self.icon_base_path, icon_file)
            self.add_icon_at_position(col, row, icon_file, label)

    def add_icon_at_position(self, col, row, icon_file, label):
        """Agregar un icono en una posición específica del grid"""
        if col >= self.grid_cols or row >= self.grid_rows:
            return False

        icon_path = os.path.join(self.icon_base_path, icon_file)
        if not os.path.exists(icon_path):
            return self.add_icon_at_position_with_default(col, row, label)

        cell_x = col * self.icon_width
        cell_y = row * self.icon_height

        icon_x = cell_x + (self.icon_width - self.icon_size) // 2
        icon_y = cell_y + (self.icon_height - self.icon_size - 20) // 2

        is_notepad = icon_file == "notepad.png"

        icon_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(icon_x, icon_y, self.icon_size, self.icon_size),
            text='',
            manager=self.manager,
            object_id=ObjectID(
                object_id='@notepad_icon' if is_notepad else f'@{label.lower()}_icon',
                class_id='#desktop_icon'
            )
        )

        label_x = cell_x + (self.icon_width - 80) // 2
        label_y = icon_y + self.icon_size + 5

        text_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(label_x, label_y, 80, 20),
            text=label,
            manager=self.manager,
            object_id=ObjectID(object_id=f'@{label.lower()}_label',
                               class_id='#desktop_label')
        )

        self.icons.append({
            'button': icon_button,
            'label': text_label,
            'col': col,
            'row': row,
            'icon_file': icon_file,
            'name': label
        })

        return True

    def add_random_icons(self, count=5):
        """Agregar iconos aleatorios en posiciones vacías"""
        empty_positions = self.get_empty_positions()

        if len(empty_positions) == 0:
            return

        positions_to_fill = random.sample(empty_positions, min(count, len(empty_positions)))

        for col, row in positions_to_fill:
            icon_file, default_name = random.choice(self.available_icons)

            self.add_icon_at_position(col, row, icon_file, default_name)

    def get_empty_positions(self):
        """Obtener posiciones vacías en el grid"""
        occupied_positions = {(icon['col'], icon['row']) for icon in self.icons}
        empty_positions = []

        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                if (col, row) not in occupied_positions:
                    empty_positions.append((col, row))

        return empty_positions
    
    def get_current_minute(self):
        """Obtiene el minuto actual desde el inicio"""
        elapsed_seconds = time.time() - self.start_time
        
        if 0 <= elapsed_seconds < env.FIRST_STAGE_TIME:
            return 1
        elif elapsed_seconds < env.SECOND_STAGE_TIME:
            return 2
        else:
            return 3

    def fill_screen_gradually(self):
        """Llenar la pantalla gradualmente con iconos"""
        empty_count = len(self.get_empty_positions())
        if (1 - (empty_count / (self.grid_cols * self.grid_rows))) < self.weight_icon_screen.get(self.get_current_minute(), 0):
            # Agregar entre 1 y 3 iconos cada vez (una fila completa máximo)
            icons_to_add = min(random.randint(1, 3), empty_count)
            self.add_random_icons(icons_to_add)

    def handle_icon_click(self, event_ui_object_id):
        for icon in self.icons:
            if icon['button'].object_ids[-1] == event_ui_object_id:
                return icon['name']
        return None

    def update_resolution(self, new_width, new_height):
        self.window_width = new_width
        self.window_height = new_height
        self.icon_width = new_width // self.grid_cols
        self.icon_height = new_height // self.grid_rows

    def cleanup(self):
        """Limpiar iconos al cambiar resolución""" #Al final como siempre sera 1920x1080 da igual
        for icon in self.icons:
            icon['button'].kill()
            icon['label'].kill()
        self.icons.clear()

def create_desktop_background(width, height):
    """Crear el fondo de escritorio estilo Windows XP"""
    try:
        background_image = pygame.image.load("windows_bg/background.png")
        background = pygame.transform.scale(background_image, (width, height))
        print("Imagen de fondo de Windows cargada correctamente")
        return background
    except (pygame.error, FileNotFoundError) as e:
        print(f"No se pudo cargar la imagen de fondo: {e}")
        background = pygame.Surface((width, height))
        background.fill((135, 206, 235))
        return background

def create_default_icon_files():
    """Crear archivos de iconos por defecto si no existen"""
    icon_dir = "ui_icons"

    # Lista de iconos iniciales
    essential_icons = [
        "canvas.png", "whatsapp.png", "gmail.png",
        "zoom.png"
    ]

    for icon_name in essential_icons:
        icon_path = os.path.join(icon_dir, icon_name)
        if not os.path.exists(icon_path):
            create_simple_icon(icon_path, icon_name)


def create_simple_icon(filepath, icon_name):
    """Crear un icono simple con pygame"""
    pygame.init()
    surface = pygame.Surface((64, 64), pygame.SRCALPHA)
    color = (100, 100, 100)

    pygame.draw.rect(surface, color, (8, 8, 48, 48))

    pygame.image.save(surface, filepath)

