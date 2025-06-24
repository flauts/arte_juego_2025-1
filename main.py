import pygame
import pygame_gui
import time
from end import show_end_screen
from icons import IconGrid, create_desktop_background, create_default_icon_files
from apps_handler import launch_app

pygame.init()
pygame.mixer.init()
click_sound = pygame.mixer.Sound("sounds/click.wav")
error_sound = pygame.mixer.Sound("sounds/error.mp3")
pygame.display.set_caption('Mind-OS: Close the window')
click_sound.set_volume(1.0)


WINDOWS_WIDTH = 1024
WINDOWS_HEIGHT = 768

is_fullscreen = False
original_size = (WINDOWS_WIDTH, WINDOWS_HEIGHT)

window_surface = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))



# Variables globales
icon_grid = None
background = None
manager = pygame_gui.UIManager((WINDOWS_WIDTH, WINDOWS_HEIGHT), theme_path="theme.json")
last_icon_add_time = 0
icon_add_interval = 3

# Lista para manejar ventanas activas
active_windows = []
error_windows = {}  # Diccionario para trackear las ventanas de error


def toggle_fullscreen():
    global window_surface, is_fullscreen, WINDOWS_WIDTH, WINDOWS_HEIGHT, background, manager, icon_grid

    if is_fullscreen:
        # Cambiar a VENTANA
        window_surface = pygame.display.set_mode(original_size)
        WINDOWS_WIDTH, WINDOWS_HEIGHT = original_size
        is_fullscreen = False
        print("Cambiado a modo ventana")
    else:
        # Cambiar a PANTALLA COMPLETA
        window_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        WINDOWS_WIDTH, WINDOWS_HEIGHT = window_surface.get_size()
        is_fullscreen = True
        print(f"Cambiado a pantalla completa: {WINDOWS_WIDTH}x{WINDOWS_HEIGHT}")

    background = create_desktop_background(WINDOWS_WIDTH, WINDOWS_HEIGHT)

    manager.set_window_resolution((WINDOWS_WIDTH, WINDOWS_HEIGHT))

    if icon_grid:
        icon_grid.cleanup()
    icon_grid = IconGrid(manager, WINDOWS_WIDTH, WINDOWS_HEIGHT)


def initialize_desktop():
    global background, manager, icon_grid

    try:
        create_default_icon_files()
    except Exception as e:
        print(f"Error al crear iconos por defecto: {e}")

    background = create_desktop_background(WINDOWS_WIDTH, WINDOWS_HEIGHT)

    try:
        manager = pygame_gui.UIManager((WINDOWS_WIDTH, WINDOWS_HEIGHT), theme_path="theme.json")
        print("Tema cargado correctamente")
    except Exception as e:
        print(f"Error al cargar tema: {e}")
        manager = pygame_gui.UIManager((WINDOWS_WIDTH, WINDOWS_HEIGHT))
        print("Usando tema por defecto")

    icon_grid = IconGrid(manager, WINDOWS_WIDTH, WINDOWS_HEIGHT)


def handle_gradual_icon_filling():
    """Manejar el llenado gradual de iconos"""
    global last_icon_add_time

    current_time = time.time()
    if current_time - last_icon_add_time >= icon_add_interval:
        if icon_grid:
            empty_positions = icon_grid.get_empty_positions()
            if len(empty_positions) > 0:
                icon_grid.fill_screen_gradually()
                last_icon_add_time = current_time
                print(f"Iconos agregados. Posiciones vacías restantes: {len(icon_grid.get_empty_positions())}")


def handle_error_button_click(event, error_components):
    """Maneja el clic del botón OK del error"""
    if event.ui_element == error_components["ok_button"]:
        click_sound.play()
        error_components["window"].kill()
        if error_components["window"] in active_windows:
            active_windows.remove(error_components["window"])
        return True
    return False


def main():
    """Función principal"""
    global is_running, active_windows, error_windows

    initialize_desktop()

    clock = pygame.time.Clock()
    is_running = True
    start_time = time.time()

    print("""Escritorio Windows XP iniciado \n Controles:\n
        - F11: Pantalla completa/Ventana\n
        - ESC: Salir de pantalla completa""")

    while is_running:

        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time >= 300:  # 5 minutos = 300 segundos
            show_emotional_end = True
            show_end_screen(show_emotional_end)
            is_running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                show_emotional_end = True
                show_end_screen(show_emotional_end)

            # PARA MANEJAR TECLAS
            key_actions = {
                pygame.K_F11: toggle_fullscreen,
                pygame.K_ESCAPE: lambda: toggle_fullscreen() if is_fullscreen else None
            }

            if event.type == pygame.KEYDOWN:
                action = key_actions.get(event.key)
                if action:
                    action()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                button_handled = False
                for error_id, error_components in list(error_windows.items()):
                    if handle_error_button_click(event, error_components):
                        del error_windows[error_id]
                        button_handled = True
                        break

                if not button_handled and icon_grid:
                    clicked_icon = icon_grid.handle_icon_click(event.ui_object_id)
                    click_sound.play()
                    if clicked_icon:
                        print(f"¡Ejecutando aplicación: {clicked_icon}!")
                        app_components = launch_app(clicked_icon, manager, click_sound=click_sound, error_sound=error_sound)
                        if app_components and "window" in app_components:
                            active_windows.append(app_components["window"])
                            # Si es una ventana de error, agregarla al diccionario
                            if "ok_button" in app_components:
                                error_id = id(app_components["window"])
                                error_windows[error_id] = app_components

            if event.type == pygame_gui.UI_WINDOW_CLOSE:
                # Manejar cuando se cierra una ventana con la X
                for error_id, error_components in list(error_windows.items()):
                    if event.ui_element == error_components["window"]:
                        if error_components["window"] in active_windows:
                            active_windows.remove(error_components["window"])
                        del error_windows[error_id]
                        break

            manager.process_events(event)

        time_delta = clock.tick(60) / 1000.0

        handle_gradual_icon_filling()

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
