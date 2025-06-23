import pygame, sys
import pygame_gui
import time
import datetime
import math

from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements import UIStatusBar, UIProgressBar, UIScreenSpaceHealthBar, UIButton

from game_config import (
    WINDOWS_WIDTH, WINDOWS_HEIGHT, MAX_POP_UPS_STAGE_ONE,
    MAX_POP_UPS_STAGE_THREE,
    MAX_POP_UPS_STAGE_TWO, POP_UP_CHECK_INTERVAL_SECONDS_STAGE_ONE
)
from ui_manager import UIManager
from game_state import GameState

pygame.init()
pygame.display.set_caption('Quick Start')

window_surface = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
background = pygame.Surface((WINDOWS_WIDTH, WINDOWS_HEIGHT))
background.fill(pygame.Color('antiquewhite3'))
game_state = GameState()
ui_manager = UIManager((WINDOWS_WIDTH, WINDOWS_HEIGHT), theme_path="theme.json", game_state_ref=game_state)
def play(clock):
    ui_manager._create_buttons()
    is_running = True
    while is_running:
        time_delta = clock.tick(60) / 1000.0
        current_real_time = time.time()
        # Handle pop-up generation for stages
        if game_state.current_stage == 1:
            if game_state.should_check_for_popup(current_real_time, POP_UP_CHECK_INTERVAL_SECONDS_STAGE_ONE):
                if len(ui_manager.popup_manager.active_popups) < MAX_POP_UPS_STAGE_ONE:
                    new_popup_info = ui_manager.popup_manager.create_popup_for_stage(game_state.current_stage,
                                                                                      screen_size=(WINDOWS_WIDTH, WINDOWS_HEIGHT))
                    if new_popup_info:
                        new_popup_info["window"].show()
        elif game_state.current_stage == 2:
            if len(ui_manager.popup_manager.active_popups) < MAX_POP_UPS_STAGE_TWO:
                new_popup_info = ui_manager.popup_manager.create_popup_for_stage(game_state.current_stage,
                                                                                  screen_size=(WINDOWS_WIDTH, WINDOWS_HEIGHT))
                if new_popup_info:
                    new_popup_info["window"].show()
        elif game_state.current_stage == 3:
            if len(ui_manager.popup_manager.active_popups) < MAX_POP_UPS_STAGE_THREE:
                new_popup_info = ui_manager.popup_manager.create_popup_for_stage(game_state.current_stage,
                                                                                  screen_size=(WINDOWS_WIDTH, WINDOWS_HEIGHT))
                if new_popup_info:
                    new_popup_info["window"].show()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            ui_manager.process_event(event)

        # Update UI manager
        ui_manager.update(time_delta)

        # Drawing
        window_surface.blit(background, (0, 0))
        ui_manager.draw(window_surface)
        pygame.display.update()
    pygame.quit()

pygame.display.set_caption('Menu')

BG = pygame.image.load('bg/bg.png')
is_running = True

PLAY_BUTTON = UIButton(relative_rect=pygame.Rect((275, 275), (200, 70)),
                        anchors={'left':'left',
                                 'right':'right',
                                 'top':'top',
                                 'bottom':'bottom'},
                        text='PLAY',
                       manager=ui_manager.manager)

clock = pygame.time.Clock()
while is_running:
    time_delta = clock.tick(60) / 1000.0
    window_surface.blit(BG, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == PLAY_BUTTON:
                PLAY_BUTTON.kill()
                play(clock)
        ui_manager.manager.process_events(event)
        ui_manager.manager.update(time_delta)
    ui_manager.manager.draw_ui(window_surface)
    pygame.display.update()
