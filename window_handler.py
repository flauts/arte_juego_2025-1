import pygame
import pygame_gui
from pygame_gui.core import ObjectID

def open_canvas_window(manager):
    canvas_window = pygame_gui.elements.UIWindow(rect=pygame.Rect((100, 100), (400, 400)),manager=manager,
                                             window_display_title='Canvas',draggable=True,
                                                 object_id=ObjectID(object_id='@canvas_window',
                                                                    class_id="#window"))

    canvas_panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((10, 30), (380, 360)),
        manager=manager,
        container=canvas_window
    )
    return canvas_window


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

    return chat_window
    # return {
    #     'window': chat_window,
    #     'chat_display': chat_display,
    #     'message_input': message_input,
    #     'send_button': send_button,
    #     'users_list': users_list,
    #     'clear_button': clear_button,
    #     'settings_button': settings_button
    # }

#
# def open_chat_window(manager):
#     canvas_window = pygame_gui.elements.UIWindow(rect=pygame.Rect((100, 100), (400, 400)),manager=manager,
#                                              window_display_title='Chat',draggable=True,
#                                                  object_id=ObjectID(object_id='@chat_window',
#                                                                     class_id="#window"))
#     return canvas_window