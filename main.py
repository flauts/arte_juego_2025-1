import pygame
import pygame_gui
import time
from end import show_end_screen
from icons import IconGrid, create_desktop_background, create_default_icon_files
from apps_handler import launch_app
from popup_manager import PopupManager
import env_variables as env
popup_manager = None


users_array = []

current_user = {
    'username': '',
    'password': '',
    'logged_in': False
}

def show_login_screen():
    global current_user, users_array

    info = pygame.display.Info()
    login_surface = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN | pygame.NOFRAME)
    pygame.mouse.set_visible(True)  # O False, si quieres ocultar el cursor

    WINDOWS_WIDTH = info.current_w
    WINDOWS_HEIGHT = info.current_h

    pygame.display.set_caption('Mind-OS: Iniciar Sesión')
    
    background_color = (0, 32, 96)
    white = (255, 255, 255)
    light_blue = (100, 149, 237)
    dark_blue = (0, 50, 150)
    hover_blue = (120, 169, 255)
    input_bg = (240, 240, 240)
    input_border = (150, 150, 150)
    input_active_border = (0, 120, 215)
    button_shadow = (0, 0, 0, 100)
    
    try:
        title_font = pygame.font.SysFont('Arial', 48, bold=True)
        label_font = pygame.font.SysFont('Arial', 24, bold=True)
        input_font = pygame.font.SysFont('Arial', 20)
        button_font = pygame.font.SysFont('Arial', 24, bold=True)
    except:
        title_font = pygame.font.Font(None, 48)
        label_font = pygame.font.Font(None, 24)
        input_font = pygame.font.Font(None, 20)
        button_font = pygame.font.Font(None, 24)
    
    username_text = ""
    password_text = ""
    username_active = False
    password_active = False
    cursor_visible = True
    cursor_timer = 0
    
    center_x = WINDOWS_WIDTH // 2
    center_y = WINDOWS_HEIGHT // 2
    
    input_width = 300
    input_height = 40
    button_width = 200
    button_height = 50
    
    username_rect = pygame.Rect(center_x - input_width//2, center_y - 60, input_width, input_height)
    password_rect = pygame.Rect(center_x - input_width//2, center_y + 20, input_width, input_height)
    
    button_rect = pygame.Rect(center_x - button_width//2, center_y + 100, button_width, button_height)
    button_hovered = False
    
    clock = pygame.time.Clock()
    login_running = True
    
    while login_running:
        mouse_pos = pygame.mouse.get_pos()
        button_hovered = button_rect.collidepoint(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    username_active = username_rect.collidepoint(mouse_pos)
                    password_active = password_rect.collidepoint(mouse_pos)
                    
                    if button_hovered and username_text.strip() and password_text.strip():
                        try:
                            click_sound.play()
                        except:
                            pass
                        
                        current_user['username'] = username_text.strip()
                        current_user['password'] = password_text.strip()
                        current_user['logged_in'] = True
                        
                        user_entry = {
                            'username': username_text.strip(),
                            'password': password_text.strip(),
                            'login_time': time.time()
                        }
                        users_array.append(user_entry)
                        
                        print(f"Usuario agregado: {username_text}")
                        print(f"Total usuarios en array: {len(users_array)}")
                        
                        login_running = False
            
            if event.type == pygame.KEYDOWN:
                if username_active:
                    if event.key == pygame.K_BACKSPACE:
                        username_text = username_text[:-1]
                    elif event.key == pygame.K_TAB:
                        username_active = False
                        password_active = True
                    elif event.key == pygame.K_RETURN:
                        if username_text.strip() and password_text.strip():
                            current_user['username'] = username_text.strip()
                            current_user['password'] = password_text.strip()
                            current_user['logged_in'] = True
                            
                            user_entry = {
                                'username': username_text.strip(),
                                'password': password_text.strip(),
                                'login_time': time.time()
                            }
                            users_array.append(user_entry)
                            
                            login_running = False
                    else:
                        if len(username_text) < 20:
                            username_text += event.unicode
                
                elif password_active:
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    elif event.key == pygame.K_TAB:
                        password_active = False
                        username_active = True
                    elif event.key == pygame.K_RETURN:
                        if username_text.strip() and password_text.strip():
                            current_user['username'] = username_text.strip()
                            current_user['password'] = password_text.strip()
                            current_user['logged_in'] = True
                            
                            user_entry = {
                                'username': username_text.strip(),
                                'password': password_text.strip(),
                                'login_time': time.time()
                            }
                            users_array.append(user_entry)
                            
                            login_running = False
                    else:
                        if len(password_text) < 20:
                            password_text += event.unicode
        
        cursor_timer += clock.get_time()
        if cursor_timer > 500:
            cursor_visible = not cursor_visible
            cursor_timer = 0
        
        login_surface.fill(background_color)
        
        title_surface = title_font.render("Mind-OS", True, white)
        title_rect = title_surface.get_rect(center=(center_x, center_y - 160))
        login_surface.blit(title_surface, title_rect)
        
        subtitle_surface = label_font.render("Iniciar Sesión", True, light_blue)
        subtitle_rect = subtitle_surface.get_rect(center=(center_x, center_y - 125))
        login_surface.blit(subtitle_surface, subtitle_rect)
        
        username_label = label_font.render("Usuario:", True, white)
        username_label_rect = username_label.get_rect(center=(center_x, center_y - 90))
        login_surface.blit(username_label, username_label_rect)
        
        username_border_color = input_active_border if username_active else input_border
        pygame.draw.rect(login_surface, input_bg, username_rect)
        pygame.draw.rect(login_surface, username_border_color, username_rect, 2)
        
        username_display = username_text
        if username_active and cursor_visible:
            username_display += "|"
        
        username_text_surface = input_font.render(username_display, True, dark_blue)
        text_rect = username_text_surface.get_rect(midleft=(username_rect.x + 10, username_rect.centery))
        login_surface.blit(username_text_surface, text_rect)
        
        password_label = label_font.render("Contraseña:", True, white)
        password_label_rect = password_label.get_rect(center=(center_x, center_y - 10))
        login_surface.blit(password_label, password_label_rect)
        
        password_border_color = input_active_border if password_active else input_border
        pygame.draw.rect(login_surface, input_bg, password_rect)
        pygame.draw.rect(login_surface, password_border_color, password_rect, 2)
        
        password_display = "*" * len(password_text)
        if password_active and cursor_visible:
            password_display += "|"
        
        password_text_surface = input_font.render(password_display, True, dark_blue)
        text_rect = password_text_surface.get_rect(midleft=(password_rect.x + 10, password_rect.centery))
        login_surface.blit(password_text_surface, text_rect)
        
        button_enabled = bool(username_text.strip() and password_text.strip())
        button_color = hover_blue if (button_hovered and button_enabled) else light_blue
        button_text_color = white if button_enabled else (200, 200, 200)
        
        if button_enabled:
            shadow_rect = pygame.Rect(button_rect.x + 3, button_rect.y + 3, button_width, button_height)
            pygame.draw.rect(login_surface, button_shadow, shadow_rect)
        
        pygame.draw.rect(login_surface, button_color, button_rect)
        pygame.draw.rect(login_surface, white if button_enabled else input_border, button_rect, 2)
        
        button_text = button_font.render("INGRESAR", True, button_text_color)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        login_surface.blit(button_text, button_text_rect)
        
        if not username_text.strip() or not password_text.strip():
            instruction_text = "Ingresa tu usuario y contraseña para continuar"
            instruction_surface = input_font.render(instruction_text, True, (200, 200, 200))
            instruction_rect = instruction_surface.get_rect(center=(center_x, center_y + 180))
            login_surface.blit(instruction_surface, instruction_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return True

def show_loading_screen():
    
    info = pygame.display.Info()
    loading_surface = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN | pygame.NOFRAME)
    pygame.mouse.set_visible(True)  # O False, si quieres ocultar el cursor

    WINDOWS_WIDTH = info.current_w
    WINDOWS_HEIGHT = info.current_h

    pygame.display.set_caption('Mind-OS: Iniciando...')
    
    background_color = (0, 32, 96)  
    
    try:
        large_font = pygame.font.SysFont('Arial', 48, bold=True)
        medium_font = pygame.font.SysFont('Arial', 32, bold=True)
        small_font = pygame.font.SysFont('Arial', 24)
    except:
        large_font = pygame.font.Font(None, 48)
        medium_font = pygame.font.Font(None, 32)
        small_font = pygame.font.Font(None, 24)
    
    main_text = "Mind-OS"
    sub_text = "Iniciando sistema..."
    loading_text = "Por favor espere..."
    complete_text = "¡Sistema listo!"
    
    white = (255, 255, 255)
    light_blue = (100, 149, 237)
    dark_blue = (0, 50, 150)
    hover_blue = (120, 169, 255)
    button_gray = (200, 200, 200)
    button_dark_gray = (150, 150, 150)
    
    try:
        windows_start_sound.play()
    except:
        pass
    
    clock = pygame.time.Clock()
    start_time = time.time()
    loading_duration = 5.0  
    loading_complete = False
    
    dots_count = 0
    dots_timer = 0
    
    button_width = 200
    button_height = 50
    button_x = (WINDOWS_WIDTH - button_width) // 2
    button_y = WINDOWS_HEIGHT // 2 + 150
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    button_hovered = False
    
    while not loading_complete:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        
        progress = (time.time() - start_time) / loading_duration
        
        if progress >= 1.0:
            loading_complete = True
            progress = 1.0
        
        loading_surface.fill(background_color)
        
        main_surface = large_font.render(main_text, True, white)
        
        # AQUÍ ESTABA EL PROBLEMA - Se mostraba texto incorrecto durante la carga
        if not loading_complete:
            # Durante la carga - mostrar texto de iniciando
            sub_surface = small_font.render(sub_text, True, light_blue)
            
            # Animación de puntos
            dots_timer += clock.get_time()
            if dots_timer > 500:  
                dots_count = (dots_count + 1) % 4
                dots_timer = 0
            
            dots = "." * dots_count
            loading_surface_text = small_font.render(loading_text + dots, True, white)
        else:
            # Solo cuando esté completado - mostrar texto de listo
            sub_surface = medium_font.render(complete_text, True, (0, 255, 0))
            loading_surface_text = small_font.render("Haz clic en 'Iniciar' para continuar", True, white)
        
        screen_center_x = WINDOWS_WIDTH // 2
        screen_center_y = WINDOWS_HEIGHT // 2
        
        main_rect = main_surface.get_rect(center=(screen_center_x, screen_center_y - 80))
        sub_rect = sub_surface.get_rect(center=(screen_center_x, screen_center_y - 30))
        loading_rect = loading_surface_text.get_rect(center=(screen_center_x, screen_center_y + 20))
        
        loading_surface.blit(main_surface, main_rect)
        loading_surface.blit(sub_surface, sub_rect)
        loading_surface.blit(loading_surface_text, loading_rect)
        
        bar_width = 300
        bar_height = 20
        bar_x = (WINDOWS_WIDTH - bar_width) // 2
        bar_y = screen_center_y + 60
        
        pygame.draw.rect(loading_surface, (50, 50, 50), 
                       (bar_x, bar_y, bar_width, bar_height))
        
        progress_width = int(bar_width * progress)
        color = (0, 255, 0) if loading_complete else light_blue  
        pygame.draw.rect(loading_surface, color, 
                       (bar_x, bar_y, progress_width, bar_height))
        
        pygame.draw.rect(loading_surface, white, 
                       (bar_x, bar_y, bar_width, bar_height), 2)
        
        percentage = int(progress * 100)
        percent_text = small_font.render(f"{percentage}%", True, white)
        percent_rect = percent_text.get_rect(center=(screen_center_x, bar_y + bar_height + 25))
        loading_surface.blit(percent_text, percent_rect)
        
        pygame.display.flip()
        clock.tick(60)

    # Pantalla de espera después de completar la carga
    waiting_for_start = True
    
    while waiting_for_start:
        mouse_pos = pygame.mouse.get_pos()
        button_hovered = button_rect.collidepoint(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_hovered:
                    try:
                        click_sound.play()
                    except:
                        pass
                    waiting_for_start = False
        
        loading_surface.fill(background_color)
        
        main_surface = large_font.render(main_text, True, white)
        sub_surface = medium_font.render(complete_text, True, (0, 255, 0))
        instruction_surface = small_font.render("Haz clic en 'Iniciar' para continuar", True, white)
        
        main_rect = main_surface.get_rect(center=(WINDOWS_WIDTH // 2, WINDOWS_HEIGHT // 2 - 80))
        sub_rect = sub_surface.get_rect(center=(WINDOWS_WIDTH // 2, WINDOWS_HEIGHT // 2 - 30))
        instruction_rect = instruction_surface.get_rect(center=(WINDOWS_WIDTH // 2, WINDOWS_HEIGHT // 2 + 20))
        
        loading_surface.blit(main_surface, main_rect)
        loading_surface.blit(sub_surface, sub_rect)
        loading_surface.blit(instruction_surface, instruction_rect)
        
        bar_width = 300
        bar_height = 20
        bar_x = (WINDOWS_WIDTH - bar_width) // 2
        bar_y = WINDOWS_HEIGHT // 2 + 60
        
        pygame.draw.rect(loading_surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(loading_surface, (0, 255, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(loading_surface, white, (bar_x, bar_y, bar_width, bar_height), 2)
        
        percent_text = small_font.render("100%", True, white)
        percent_rect = percent_text.get_rect(center=(WINDOWS_WIDTH // 2, bar_y + bar_height + 25))
        loading_surface.blit(percent_text, percent_rect)
        
        button_color = hover_blue if button_hovered else light_blue
        button_border_color = white if button_hovered else button_gray
        
        shadow_rect = pygame.Rect(button_x + 3, button_y + 3, button_width, button_height)
        pygame.draw.rect(loading_surface, (0, 0, 0, 100), shadow_rect)
        
        pygame.draw.rect(loading_surface, button_color, button_rect)
        pygame.draw.rect(loading_surface, button_border_color, button_rect, 3)
        
        button_text = medium_font.render("INICIAR", True, white if button_hovered else dark_blue)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        loading_surface.blit(button_text, button_text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return True


pygame.init()
pygame.mixer.init()
click_sound = pygame.mixer.Sound("sounds/click.wav")
error_sound = pygame.mixer.Sound("sounds/error.mp3")
gmail_sound = pygame.mixer.Sound("sounds/gmail.mp3")
canvas_sound = pygame.mixer.Sound("sounds/canvas.mp3")
whatsapp_sound = pygame.mixer.Sound("sounds/whatsapp.mp3")
windows_not1_sound = pygame.mixer.Sound("sounds/windows-not1.mp3")
windows_not2_sound = pygame.mixer.Sound("sounds/windows-not2.mp3")
windows_start_sound = pygame.mixer.Sound("sounds/windows_start.mp3")

pygame.display.set_caption('Mind-OS: Close the window')
click_sound.set_volume(0.3)

is_fullscreen = True
info = pygame.display.Info()
window_surface = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN | pygame.NOFRAME)
pygame.mouse.set_visible(False)
WINDOWS_WIDTH, WINDOWS_HEIGHT = window_surface.get_size()
original_size = (WINDOWS_WIDTH, WINDOWS_HEIGHT)

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
    global window_surface, is_fullscreen, WINDOWS_WIDTH, WINDOWS_HEIGHT, background, manager, icon_grid, popup_manager  # Añadir popup_manager

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

    if popup_manager:
        popup_manager.cleanup()
    popup_manager = PopupManager(
        manager,
        click_sound=click_sound,
        error_sound=error_sound,
        gmail_sound=gmail_sound,
        canvas_sound=canvas_sound,
        whatsapp_sound=whatsapp_sound,
        windows_not1_sound=windows_not1_sound,
        windows_not2_sound=windows_not2_sound
    )

def initialize_desktop():
    global background, manager, icon_grid, popup_manager, last_icon_add_time, start_time

    start_time = time.time()
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

    popup_manager = PopupManager(
        manager,
        click_sound=click_sound,
        error_sound=error_sound,
        gmail_sound=gmail_sound,
        canvas_sound=canvas_sound,
        whatsapp_sound=whatsapp_sound,
        windows_not1_sound=windows_not1_sound,
        windows_not2_sound=windows_not2_sound
    )
    print("Popup manager inicializado")

def get_current_minute():
    global start_time

    """Obtiene el minuto actual desde el inicio"""
    elapsed_seconds = time.time() - start_time
    
    if 0 <= elapsed_seconds < env.FIRST_STAGE_TIME:
        return 1
    elif elapsed_seconds < env.SECOND_STAGE_TIME:
        return 2
    else:
        return 3

icon_add_time = {
    1: 5,
    2: 3,
    3: 1
}

def handle_gradual_icon_filling():
    """Manejar el llenado gradual de iconos"""
    global last_icon_add_time

    current_time = time.time()
    if current_time - last_icon_add_time >= icon_add_time.get(get_current_minute(), 5):
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

def run_mind_os():
    global is_running, active_windows, error_windows, popup_manager, start_time

    while True:  # Loop que permite reiniciar el sistema

        if not show_login_screen():
            break  # Usuario cerró la ventana en login

        print(f"Usuario logueado: {current_user['username']}")
        print(f"Total usuarios registrados: {len(users_array)}")

        if not show_loading_screen():
            break

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

            if elapsed_time >= env.FINAL_STAGE_TIME:
                show_emotional_end = True
                show_end_screen(show_emotional_end, elapsed_time)
                is_running = False
                break  # Termina el ciclo interno (escritorio) y reinicia desde login


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                    show_emotional_end = True
                    show_end_screen(show_emotional_end, elapsed_time)

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

                    # Manejar clics en popups PRIMERO
                    if popup_manager and popup_manager.handle_popup_click(event):
                        button_handled = True

                    # Luego manejar errores existentes
                    if not button_handled:
                        for error_id, error_components in list(error_windows.items()):
                            if handle_error_button_click(event, error_components):
                                del error_windows[error_id]
                                button_handled = True
                                break

                    # Finalmente manejar iconos
                    if not button_handled and icon_grid:
                        clicked_icon = icon_grid.handle_icon_click(event.ui_object_id)
                        click_sound.play()
                        if clicked_icon:
                            print(f"¡Ejecutando aplicación: {clicked_icon}!")
                            app_components = launch_app(clicked_icon, manager, click_sound=click_sound,
                                                        error_sound=error_sound)
                            if app_components and "window" in app_components:
                                active_windows.append(app_components["window"])
                                # Si es una ventana de error, agregarla al diccionario
                                if "ok_button" in app_components:
                                    error_id = id(app_components["window"])
                                    error_windows[error_id] = app_components

                if event.type == pygame_gui.UI_WINDOW_CLOSE:
                    # Manejar cierre de popups
                    if popup_manager and popup_manager.handle_popup_close(event):
                        pass
                    else:
                        for error_id, error_components in list(error_windows.items()):
                            if event.ui_element == error_components["window"]:
                                if error_components["window"] in active_windows:
                                    active_windows.remove(error_components["window"])
                                del error_windows[error_id]
                                break
                if popup_manager:
                    popup_manager.update()

                    # Debug info (opcional - puedes comentar esto después de probar)
                    debug_info = popup_manager.get_debug_info()
                    if int(debug_info["elapsed_time"]) % 10 == 0 and int(debug_info["elapsed_time"]) > 0:
                        print(
                            f"Minuto: {debug_info['minute']}, Intervalo: {debug_info['interval']}, Popups activos: {debug_info['active_popups']}")

                manager.process_events(event)       
                
            time_delta = clock.tick(60) / 1000.0
            handle_gradual_icon_filling()
            if popup_manager:
                popup_manager.update()
            manager.update(time_delta)

            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.update()



if __name__ == "__main__":
    run_mind_os()
    pygame.quit()
