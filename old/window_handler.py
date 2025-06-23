import random
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
import json

POPUP_PATH = "../popups.json"

with open(POPUP_PATH, "r", encoding="utf-8") as f:
    POPUP_DATA = json.load(f)

def open_canvaswindow(manager):
    canvas_window = pygame_gui.elements.UIWindow(rect=pygame.Rect((100, 100), (400, 400)),manager=manager,
                                             window_display_title='Canvas',draggable=True,
                                                 object_id=ObjectID(object_id='@canvas_window',
                                                                    class_id="#window"))

    canvas_panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((10, 30), (380, 360)),
        manager=manager,
        container=canvas_window
    )
    return {
        "window": canvas_window,
    }


def open_chat_window(manager):
    # Create the main chat window
    chat_window = pygame_gui.elements.UIWindow(
        rect=pygame.Rect((100, 100), (450, 500)),
        manager=manager,
        window_display_title='Chat Room',
        draggable=True,
        object_id=ObjectID(object_id='@chat_window', class_id="#window")
    )

    # Create main panel inside the window
    main_panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((5, 30), (440, 465)),
        manager=manager,
        container=chat_window
    )

    # Chat display area (scrollable text box for messages)
    chat_display = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((10, 10), (420, 350)),
        html_text="<b>Welcome to the chat!</b><br>"
                  "System: Chat room initialized<br>"
                  "<font color='#0066CC'>User1:</font> Hello everyone!<br>"
                  "<font color='#CC6600'>User2:</font> Hey there!<br>",
        manager=manager,
        container=main_panel
    )

    # Input field for typing messages
    message_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((10, 370), (320, 30)),
        manager=manager,
        container=main_panel,
        placeholder_text="Type your message here..."
    )

    # Send button
    send_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((340, 370), (80, 30)),
        text='Send',
        manager=manager,
        container=main_panel
    )

    # Online users list (optional)
    users_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((10, 410), (100, 20)),
        text='Online Users:',
        manager=manager,
        container=main_panel
    )

    users_list = pygame_gui.elements.UISelectionList(
        relative_rect=pygame.Rect((120, 410), (150, 45)),
        item_list=['User1', 'User2', 'User3'],
        manager=manager,
        container=main_panel
    )

    # Clear chat button
    clear_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((280, 410), (80, 25)),
        text='Clear',
        manager=manager,
        container=main_panel
    )

    # Settings button
    settings_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((280, 435), (80, 20)),
        text='Settings',
        manager=manager,
        container=main_panel
    )

    return {
        'window': chat_window,
        'chat_display': chat_display,
        'message_input': message_input,
        'send_button': send_button,
        'users_list': users_list,
        'clear_button': clear_button,
        'settings_button': settings_button
    }


def create_random_ui_message(manager, popup_data,window_size=(300, 150), screen_size=(800, 600)):

    max_x = screen_size[0] - window_size[0]
    max_y = screen_size[1] - window_size[1]
    x = random.randint(0, max_x)
    y = random.randint(0, max_y)

    rect = pygame.Rect((x, y), window_size)
    # id = random.randint(0, 1000000)
    popup = random.choice(popup_data)
    title = popup.get("title", "Mensaje")
    message = "<font face='retro'>" + popup.get("message", "") + "</font>"

    # Crear ventana de mensaje UIMessageWindow
    message_window = pygame_gui.elements.UIWindow(
        rect=rect,
        manager=manager,
        window_display_title=title,
        object_id=ObjectID(object_id=f"window_{popup["id"]}", class_id='#message_window'),
        visible=False
    )

    text = pygame_gui.elements.UITextBox(
        html_text=message,
        relative_rect=pygame.Rect((10, 10), (window_size[0] - 20, window_size[1] - 20)),
        manager=manager,
        container=message_window,
        object_id=ObjectID(object_id=f"window_text_{popup["id"]}", class_id='#popup_text')
    )
    dismiss_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((-90, -30), (70, 25)),
        text='Dismiss',
        manager=manager,
        container=message_window,
        anchors={'right':'right',
                 'bottom':'bottom'},
        object_id=ObjectID(object_id=f"window_dismiss_button_{popup["id"]}", class_id='#dismiss_button')
    )

    accept_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, -30), (70, 25)),
        text='Aceptar',
        manager=manager,
        container=message_window,
        anchors={'left':'left',
                 'bottom':'bottom'},
        object_id=ObjectID(object_id=f"window_accept_button_{popup["id"]}", class_id='#accept_button')
    )
    return {
        'window': message_window,
        'text': text,
        'dismiss_button': dismiss_button,
        'accept_button': accept_button,
    }

import random

estado_jugador = {}

def create_popup_from_stage(manager, stage):
    available_popups = POPUP_DATA[f"stage_{stage}"]
    return create_random_ui_message(manager,available_popups)
