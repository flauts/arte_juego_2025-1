import pygame
import pygame_gui
import time
import sys
import env_variables as env

WIDTH, HEIGHT = 1024, 768
TEXT_COLOR = (220, 220, 220)
BACKGROUND_COLOR = (0, 0, 0)
FONT_SIZE = 48
FONT_TYPE = 'Courier New'
TYPING_SPEED_SECONDS = 0.08
FINAL_WAIT_SECONDS = 7

CURSOR_BLINK_SPEED = 0.5  # segundos entre parpadeos
CURSOR_CHAR = "|"

ERROR_COLOR = (255, 0, 0)
ERROR_UNDERLINE_THICKNESS = 2

TIME_BETWEEN_WORDS = 2.0  # en segundos

pygame.mixer.init()
typing_sound = pygame.mixer.Sound("sounds/tecleo.wav")

def show_end_screen(is_emotional_end: bool, elapsed_seconds: float):
    if not is_emotional_end:
        print("Cierre rápido solicitado. La aplicación terminará.")
        pygame.quit()
        sys.exit()
    ERROR_WORD = "$$$$$"
    
    if 0 <= elapsed_seconds < env.FIRST_STAGE_TIME:
        FIRST_PART = "¿Por qué apagaste?"
        SECOND_PART = " Aún quedan tareas pendientes."
    elif elapsed_seconds < env.SECOND_STAGE_TIME:
        FIRST_PART = ". . ."
        SECOND_PART = " Tenía más espectativas."
    else:
        FIRST_PART = "Apagar no siempre es rendirse."
        SECOND_PART = " A veces es cuidarse."

    pygame.init()

    try:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        width, height = screen.get_size()
        pygame.display.set_caption("Apagando...")
        pygame.mouse.set_visible(False)
    except pygame.error as e:
        print(f"No se pudo establecer el modo de pantalla completa: {e}. Usando ventana.")
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        width, height = WIDTH, HEIGHT

    try:
        font = pygame.font.SysFont(FONT_TYPE, FONT_SIZE)
    except:
        print(f"Fuente '{FONT_TYPE}' no encontrada. Usando fuente por defecto.")
        font = pygame.font.Font(None, FONT_SIZE + 10)

    displayed_text = ""
    running = True
    clock = pygame.time.Clock()

    def draw_text_with_error_underline(text, show_error=False):
        screen.fill(BACKGROUND_COLOR)
        text_surface = font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(width / 2, height / 2))
        screen.blit(text_surface, text_rect)

    # Fase 1: Escribir la primera parte
    typing_sound.play()
    for i in range(len(FIRST_PART)):
        if not running: break

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break

        displayed_text += FIRST_PART[i]
        show_error = ERROR_WORD in displayed_text and displayed_text.endswith(ERROR_WORD)
        draw_text_with_error_underline(displayed_text, show_error)

        pygame.display.flip()
        time.sleep(TYPING_SPEED_SECONDS)

    typing_sound.stop()

    # Fase 2: Cursor parpadeante
    if running:
        start_wait_time = time.time()
        cursor_visible = True
        last_cursor_toggle = time.time()

        while running and (time.time() - start_wait_time) < TIME_BETWEEN_WORDS:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    break

            if time.time() - last_cursor_toggle >= CURSOR_BLINK_SPEED:
                cursor_visible = not cursor_visible
                last_cursor_toggle = time.time()

            display_text = displayed_text + (CURSOR_CHAR if cursor_visible else "")
            draw_text_with_error_underline(display_text, True)
            pygame.display.flip()
            clock.tick(60)

    # Fase 3: Mostrar segunda parte
    typing_sound.play()
    if running:
        for i in range(len(SECOND_PART)):
            if not running: break

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    break

            displayed_text += SECOND_PART[i]
            draw_text_with_error_underline(displayed_text, False)
            pygame.display.flip()
            time.sleep(TYPING_SPEED_SECONDS)
    typing_sound.stop()
    
    if running:
        time.sleep(FINAL_WAIT_SECONDS)

    pygame.quit()
    sys.exit()

# QUITEN EL COMENTARIO DE ESTO DE ABAJO PARA VER COMO SE VE EL CONTENIDO FINAL


# def run_test_environment():
#     pygame.init()
#
#     test_window_size = (800, 600)
#     window_surface = pygame.display.set_mode(test_window_size)
#     pygame.display.set_caption("Prueba de Pantalla Final")
#
#     manager = pygame_gui.UIManager(test_window_size)
#
#     test_button = pygame_gui.elements.UIButton(
#         relative_rect=pygame.Rect((250, 250), (300, 100)),
#         text='Probar Final Emocional',
#         manager=manager
#     )
#
#     clock = pygame.time.Clock()
#     is_running_test = True
#
#     print("\nVentana de prueba iniciada.")
#     print("Haz clic en el botón para ejecutar 'show_end_screen(True)'.")
#
#     while is_running_test:
#         time_delta = clock.tick(60) / 1000.0
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 is_running_test = False
#
#             if event.type == pygame_gui.UI_BUTTON_PRESSED:
#                 if event.ui_element == test_button:
#                     is_running_test = False  # Cierra la ventana de prueba
#                     # Llama a la función que queremos probar
#                     show_end_screen(is_emotional_end=True)
#
#             manager.process_events(event)
#
#         manager.update(time_delta)
#
#         window_surface.fill((40, 40, 50))
#         manager.draw_ui(window_surface)
#
#         pygame.display.update()
#
#     pygame.quit()
#
# if __name__ == "__main__":
#     tiempo_total = 50
#     show_end_screen(True, tiempo_total)