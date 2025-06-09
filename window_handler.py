import pygame
import pygame_gui
from pygame_gui.core import ObjectID

def open_canvas_window(manager):
    canvas_window = pygame_gui.elements.UIWindow(rect=pygame.Rect((100, 100), (400, 400)),manager=manager,
                                             window_display_title='Canvas',draggable=True,
                                                 object_id=ObjectID(object_id='@canvas_window',
                                                                    class_id="#window"))
    return canvas_window


def open_chat_window(manager):
    canvas_window = pygame_gui.elements.UIWindow(rect=pygame.Rect((100, 100), (400, 400)),manager=manager,
                                             window_display_title='Chat',draggable=True,
                                                 object_id=ObjectID(object_id='@chat_window',
                                                                    class_id="#window"))
    return canvas_window