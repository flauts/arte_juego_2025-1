import pygame
import pygame_gui

def launch_app(app_name, manager):
    """Lanza la aplicación correspondiente al nombre"""
    if app_name.lower() == "whatsapp":
        return launch_whatsapp(manager)
    # Aquí puedes agregar más aplicaciones como elif
    else:
        print(f"[AppsHandler] No se reconoce la aplicación: {app_name}")
        return None

##def para cada uno con launch_appname

def launch_whatsapp(manager):
    """Simulación simple de una app estilo WhatsApp"""
    # Crear una ventana flotante tipo chat
    window_rect = pygame.Rect(300, 200, 400, 300)
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
