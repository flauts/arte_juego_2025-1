import pygame
import pygame_gui
import time
import sys

WIDTH, HEIGHT = 1024, 768
TEXT_COLOR = (220, 220, 220)
BACKGROUND_COLOR = (0, 0, 0)
FONT_SIZE = 48
FONT_TYPE = 'Courier New'
TYPING_SPEED_SECONDS = 0.08
FINAL_WAIT_SECONDS = 7

CURSOR_BLINK_SPEED = 0.5  # segundos entre parpadeos
CURSOR_CHAR = "|"

ERROR_COLOR = (255, 0, 0)  # Rojo para el subrayado de error
ERROR_UNDERLINE_THICKNESS = 2

# Texto dividido en dos partes
FIRST_PART = "Apagar no siempre es rendirse."
SECOND_PART = " A veces es cuidarse."
ERROR_WORD = "rendirse"  # Palabra error

# El T que peiste
T = 3.0  # en segundos


def show_end_screen(is_emotional_end: bool):
    if not is_emotional_end:
        print("Cierre rápido solicitado. La aplicación terminará.")
        pygame.quit()
        sys.exit()

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

        if show_error and ERROR_WORD in text:
            # Encontrar la posición de la palabra con error
            error_word_start = text.find(ERROR_WORD)
            if error_word_start != -1:
                # Calcular posición del subrayado
                text_before_error = text[:error_word_start]
                error_word_text = ERROR_WORD

                # Obtener dimensiones del texto antes de la palabra con error
                before_surface = font.render(text_before_error, True, TEXT_COLOR)
                error_surface = font.render(error_word_text, True, TEXT_COLOR)

                # Calcular posición del subrayado
                underline_start_x = text_rect.left + before_surface.get_width()
                underline_end_x = underline_start_x + error_surface.get_width()
                underline_y = text_rect.bottom - 5

                # Dibujar subrayado ondulado (simulado con líneas pequeñas)
                for x in range(underline_start_x, underline_end_x, 3):
                    if (x - underline_start_x) % 6 < 3:
                        pygame.draw.line(screen, ERROR_COLOR,
                                         (x, underline_y),
                                         (x + 2, underline_y + ERROR_UNDERLINE_THICKNESS),
                                         ERROR_UNDERLINE_THICKNESS)
                    else:
                        pygame.draw.line(screen, ERROR_COLOR,
                                         (x, underline_y + ERROR_UNDERLINE_THICKNESS),
                                         (x + 2, underline_y),
                                         ERROR_UNDERLINE_THICKNESS)

    # Fase 1: Escribir la primera parte
    for i in range(len(FIRST_PART)):
        if not running: break

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break

        displayed_text += FIRST_PART[i]

        # Mostrar error de ortografía solo cuando se ha escrito la palabra completa
        show_error = ERROR_WORD in displayed_text and displayed_text.endswith(ERROR_WORD)
        draw_text_with_error_underline(displayed_text, show_error)

        pygame.display.flip()
        time.sleep(TYPING_SPEED_SECONDS)

    # Fase 2: Mostrar cursor parpadeante durante el tiempo T (manteniendo el error)
    if running:
        start_wait_time = time.time()
        cursor_visible = True
        last_cursor_toggle = time.time()

        while running and (time.time() - start_wait_time) < T:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    break

            # Alternar visibilidad del cursor
            if time.time() - last_cursor_toggle >= CURSOR_BLINK_SPEED:
                cursor_visible = not cursor_visible
                last_cursor_toggle = time.time()

            # Dibujar texto con cursor y error
            display_text = displayed_text + (CURSOR_CHAR if cursor_visible else "")
            draw_text_with_error_underline(display_text, True)  # Siempre mostrar error durante la espera
            pygame.display.flip()

            clock.tick(60)

    if running:
        for i in range(len(SECOND_PART)):
            if not running: break

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    break

            displayed_text += SECOND_PART[i]
            draw_text_with_error_underline(displayed_text, False)  # No mostrar error en la fase final
            pygame.display.flip()
            time.sleep(TYPING_SPEED_SECONDS)

    # Espera final
    if running:
        time.sleep(FINAL_WAIT_SECONDS)

    pygame.quit()
    sys.exit()

# QUITEN EL COMENTARIO DE ESTO DE ABAJO PARA VER COMO SE VE EL CONTENIDO FINAL

#
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
# if __name__ == '__main__':
#     # Al ejecutar este script directamente, se llamará a la función de prueba.
#     run_test_environment()