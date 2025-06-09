import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from window_handler import *

pygame.init()
pygame.display.set_caption('Quick Start')
WINDOWS_WIDTH = 800
WINDOWS_HEIGHT = 600

window_surface = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))

background = pygame.Surface((WINDOWS_WIDTH, WINDOWS_HEIGHT))

background.fill(pygame.Color('antiquewhite3'))

manager = pygame_gui.UIManager((WINDOWS_WIDTH, WINDOWS_HEIGHT   ), theme_path="theme.json")

chat_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (40, 40)),
                                            text='',
                                            manager=manager,
                                           object_id=ObjectID(object_id='@chat_icon',
                                                              class_id='#icon'))

canvas_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 275), (40, 40)),
                                            text='',
                                            manager=manager,
                                             object_id=ObjectID(object_id='@canvas_icon',
                                                              class_id='#icon'),
                                             )

windows = []
clock = pygame.time.Clock()
is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_object_id.endswith("_icon"):
                icon_name = event.ui_object_id.split("_")[0][1:]
                opened = False
                for w in windows:
                    if w.object_ids[0].split("_")[0][1:] == icon_name:  #w.object_ids list of object ids of hierarchy
                        opened = True
                if not opened:
                    if icon_name == "chat":
                        windows.append(open_chat_window(manager))
                    elif icon_name == "canvas":
                        windows.append(open_canvas_window(manager))
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            for w in windows:
                if w.object_ids[0] == event.ui_element.object_ids[0]:
                    windows.remove(w)
                    break
        manager.process_events(event)
    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    pygame.display.update()