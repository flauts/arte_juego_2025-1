import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from content_generator import generate_note_content as generate_content
import random

def launch_app(app_name, manager, click_sound=None, error_sound=None):
    """Lanza la aplicación correspondiente al nombre"""

    notes_apps = [
        "apuntes_algoritmos",
        "tareas_matematica_discreta",
        "resumen_redes",
        "repaso_final_bd",
        "ejercicios_lógica",
        "proyecto_ia",
        "quizs_historia",
        "clase_etica",
        "apuntes_circuitos",
        "resumen_fisica",
        "simulacro_parcial",
        "preguntas_orales",
        "notas_metodología",
        "apuntes_tesis",
        "pendientes_semanales",
        "ideas_app",
        "resumen_libro",
        "glosario_sistemas",
        "resumen_normas_apa",
        "borrador_ensayo",
        "tareas_prog2",
        "lecturas_digitales",
        "mapa_mental",
        "listas_de_verificación",
        "examen_pasado_compi",
        "profe_comentarios",
        "ensayo_filosofia",
        "notas_reunión_grupo",
        "resumen_clase_28_mayo",
        "guias_de_laboratorio",
        "preparación_sustitutorio",
        "plan_estudio_junio",
        "tareas_debidas",
        "consultas_dudas",
        "lectura_semana4",
        "script_prueba_sql",
        "errores_comunes_cpp",
        "sintaxis_python",
        "esquema_memo",
        "pasos_para_instalar",
        "código_fuente_demo",
        "definiciones_clave",
        "practica_logica",
        "problemas_modelados",
        "resumen_cpp_intermedio",
        "tips_presentacion",
        "casos_estudio",
        "fechas_importantes",
        "bitacora_progreso",
        "metas_mensuales"
    ]

    app_name_l = app_name.lower()

    if app_name_l == "whatsapp":
        return launch_whatsapp(manager)
    elif app_name_l == "gmail":
        return launch_error(manager, error_sound)
    elif app_name_l == "canvas":
        return launch_error(manager, error_sound)
    elif app_name_l in notes_apps:
        return launch_note(manager, app_name_l)
    else:
        return launch_error(manager,error_sound)

##def para cada uno con launch_appname

def launch_error(manager, error_sound=None):
    """Lanza una ventana de error estilo Windows XP clásico en posición aleatoria"""
    if error_sound:
        error_sound.play()

    # Obtener dimensiones de la pantalla (asumiendo resolución común)
    screen_width = 1920
    screen_height = 1080

    error_width = 340
    error_height = 170

    # Generar posición aleatoria (evitando que se salga de pantalla)
    random_x = random.randint(0, screen_width - error_width)
    random_y = random.randint(0, screen_height - error_height)

    # Crear ventana de error en posición aleatoria
    window_rect = pygame.Rect(random_x, random_y, error_width, error_height)

    # Resto del código igual...
    error_window = pygame_gui.elements.UIWindow(
        rect=window_rect,
        manager=manager,
        window_display_title="Error",
        object_id=ObjectID(class_id='#error_window'),
        resizable=False
    )

    # Panel principal con fondo gris claro
    main_panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect(0, 0, 340, 145),
        manager=manager,
        container=error_window,
        object_id=ObjectID(class_id='#error_main_panel')
    )
    #
    # second_panel = pygame_gui.elements.UIPanel(
    #     relative_rect=pygame.Rect(0, 90, 340, 145),
    #     manager=manager,
    #     container=error_window,
    #     object_id=ObjectID(class_id='#error_second_panel')
    # )
    # me parece que no sirve xd

    # Crear el icono de error usando la imagen x.png (ahora como UIImage)
    error_icon = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect(20, 20, 55, 55),
        image_surface=pygame.image.load("ui_icons/x.png"),
        manager=manager,
        container=main_panel,
        object_id=ObjectID(class_id='#error_icon')
    )

    # Texto del error
    error_text = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(65, 35, 250, 25),
        text="Un error desconocido ha ocurrido.",
        manager=manager,
        container=main_panel,
        object_id=ObjectID(class_id='#error_text')
    )

    # Botón OK centrado en la parte inferior
    ok_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(130, 100, 75, 23),
        text="OK",
        manager=manager,
        container=main_panel,
        object_id=ObjectID(class_id='#error_ok_button')
    )

    return {
        "window": error_window,
        "panel": main_panel,
        # "bg_panel_1": second_panel,
        "icon": error_icon,
        "text": error_text,
        "ok_button": ok_button
    }

#lo mismo para gmail y las apss verdadermente funcionales
def launch_whatsapp(manager):
    """Simulación simple de una app estilo WhatsApp"""
    # Crear una ventana flotante tipo chat
    window_rect = pygame.Rect(300, 20, 400, 300)
    window = pygame_gui.elements.UIWindow(rect=window_rect,
                                          manager=manager,
                                          window_display_title="WhatsApp")

    chat_log = pygame_gui.elements.UITextBox(
        html_text="👤 Juan: ¡Hola!<br>👤 Tú: ¡Hola, Juan!",
        relative_rect=pygame.Rect(10, 10, 380, 180),
        manager=manager,
        container=window,
        object_id="#whatsapp_chat_log"
    )

    input_box = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(10, 200, 280, 30),
        manager=manager,
        container=window
    )

    send_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(300, 200, 80, 30),
        text="Enviar",
        manager=manager,
        container=window
    )

    return {
        "window": window,
        "chat_log": chat_log,
        "input_box": input_box,
        "send_button": send_button
    }




def launch_note(manager, file_name):
        """Simula una aplicación de bloc de notas con el nombre del archivo en una posición aleatoria"""

        content = generate_content(file_name)

        # Dimensiones de la ventana y de la pantalla
        window_width = 600
        window_height = 450
        screen_width = 1920
        screen_height = 1080

        # Generar posición aleatoria que no se salga de la pantalla
        random_x = random.randint(0, screen_width - window_width)
        random_y = random.randint(0, screen_height - window_height)

        # Crear la ventana tipo bloc de notas en posición aleatoria
        window_rect = pygame.Rect(random_x, random_y, window_width, window_height)
        window = pygame_gui.elements.UIWindow(
            rect=window_rect,
            manager=manager,
            window_display_title=f"{file_name.replace('_', ' ').title()}.txt",
            object_id=ObjectID(class_id='#notepad_window', object_id=file_name)
        )

        # Área de texto que simula los apuntes
        text_area = pygame_gui.elements.UITextBox(
            html_text=f"<pre>{content}</pre>",
            relative_rect=pygame.Rect(0, 0, window_width+20, window_height+10),
            manager=manager,
            container=window,
            object_id="#note_text_area"
        )

        return {
            "window": window,
            "text_area": text_area
        }
