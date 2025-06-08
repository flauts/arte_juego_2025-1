import pygame
import pygame_gui
from pygame_gui.core import ObjectID

pygame.init()
pygame.display.set_caption('Quick Start')
WINDOWS_WIDTH = 800
WINDOWS_HEIGHT = 600

window_surface = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))

background = pygame.Surface((WINDOWS_WIDTH, WINDOWS_HEIGHT))

background.fill(pygame.Color('antiquewhite3'))

manager = pygame_gui.UIManager((WINDOWS_WIDTH, WINDOWS_HEIGHT   ), theme_path="theme.json")

chat_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                            text='',
                                            manager=manager,
                                           object_id=ObjectID(object_id='@chat_button',
                                                              class_id='#button'))
canvas_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 275), (50, 50)),
                                            text='',
                                            manager=manager,
                                             object_id=ObjectID(object_id='@canvas_button',
                                                              class_id='#button'))

clock = pygame.time.Clock()
is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == chat_button:
                print('Chat pressed!')
        manager.process_events(event)
    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    pygame.display.update()