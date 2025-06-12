import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from window_handler import *
import math
pygame.init()
pygame.display.set_caption('Quick Start')
WINDOWS_WIDTH = 800
WINDOWS_HEIGHT = 600
CENTER = (750, 100)
RADIUS = 50


def draw_analog_clock(surface, time_value, center=(750, 100), radius=50):    # Draw clock face
    pygame.draw.circle(surface, pygame.Color("antiquewhite"), center, radius)
    pygame.draw.circle(surface, pygame.Color("black"), center, radius, 2)

    hour = time_value.hour % 12
    minute = time_value.minute

    hour_angle = (360 / 12) * hour - 90
    minute_angle = (360 / 60) * minute - 90

    hour_x = CENTER[0] + int(RADIUS * 0.5 * math.cos(math.radians(hour_angle)))
    hour_y = CENTER[1] + int(RADIUS * 0.5 * math.sin(math.radians(hour_angle)))

    minute_x = CENTER[0] + int(RADIUS * 0.8 * math.cos(math.radians(minute_angle)))
    minute_y = CENTER[1] + int(RADIUS * 0.8 * math.sin(math.radians(minute_angle)))

    pygame.draw.line(surface, pygame.Color("black"), CENTER, (hour_x, hour_y), 4)
    pygame.draw.line(surface, pygame.Color("gray"), CENTER, (minute_x, minute_y), 2)


window_surface = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))

background = pygame.Surface((WINDOWS_WIDTH, WINDOWS_HEIGHT))

background.fill(pygame.Color('antiquewhite3'))

manager = pygame_gui.UIManager((WINDOWS_WIDTH, WINDOWS_HEIGHT   ), theme_path="../theme.json")

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
import time
import datetime

in_game_time = datetime.datetime(2024, 1, 1, 8, 0)  # Starts at 08:00
etapa = 1
K_minutes = 2  # cada cuántos minutos mostrar
K_seconds = 2*5*(1/etapa)
start_time = time.time()
current_time = time.time()
last_message_time = current_time

pop_up_windows_ids = []
pop_up_windows = []
windows = []
clock = pygame.time.Clock()

estado_jugador = {}

is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED: #normal icon window close and open
            if event.ui_object_id.endswith("_icon"):
                icon_name = event.ui_object_id.split("_")[0][1:]
                opened = False
                for w in windows:
                    if w["window"].object_ids[0].split("_")[0][1:] == icon_name:  #w.object_ids list of object ids of hierarchy
                        opened = True
                if not opened:
                    if icon_name == "chat":
                        windows.append(open_chat_window(manager))
                    elif icon_name == "canvas":
                        windows.append(open_canvas_window(manager))
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            for w in windows:
                if w["window"].object_ids[0] == event.ui_element.object_ids[0]:
                    windows.remove(w)
                    break
        if event.type == pygame_gui.UI_BUTTON_PRESSED: #pop up window close
            if event.ui_element.text == "Aceptar":
                for w in pop_up_windows:
                    if event.ui_element.object_ids[0] in pop_up_windows_ids:
                        pop_up_windows_ids.remove(w["window"].object_ids[0])
                        pop_up_windows.remove(w)
                        w["window"].kill()
                        break
                in_game_time+=datetime.timedelta(minutes=5*etapa)
            elif event.ui_element.text == "Dismiss":
                for w in pop_up_windows:
                    if w["window"].object_ids[0] == event.ui_element.object_ids[0]:
                        pop_up_windows.remove(w)
                        pop_up_windows_ids.remove(w["window"].object_ids[0])
                        w["window"].kill()
                        break

        manager.process_events(event)
    elapsed = time.time() - start_time
    if elapsed > 180:
        etapa = 3
    elif elapsed > 60:
        etapa = 2
    else:
        etapa = 1
    current_time = time.time()
    if current_time - last_message_time > K_seconds:
        if etapa == 1:
            if len(pop_up_windows) < 2:
                pop_up = create_popup_from_stage(manager, etapa)
                pop_up["window"].show()
                pop_up_windows.append(pop_up)
                pop_up_windows_ids.append(pop_up["window"].object_ids[0])
                last_message_time = current_time
            last_message_time = current_time
        elif etapa == 2:
            pass
        elif etapa == 3:
            pass
    manager.update(time_delta)
    in_game_time+=datetime.timedelta(seconds=0.25*etapa)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    draw_analog_clock(window_surface, in_game_time)
    pygame.display.update()