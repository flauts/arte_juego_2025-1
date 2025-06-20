

# play.py
import pygame, sys
import pygame_gui
import time
import datetime
import math # ADD THIS IMPORT

from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements import UIStatusBar, UIProgressBar, UIScreenSpaceHealthBar, UIButton

from game_config import (
    WINDOWS_WIDTH, WINDOWS_HEIGHT, POP_UP_CHECK_INTERVAL_SECONDS_STAGE_TWO,POP_UP_CHECK_INTERVAL_SECONDS_STAGE_THREE, MAX_POP_UPS_STAGE_ONE,
    WELLNESS_THRESHOLD_LOW, WELLNESS_THRESHOLD_CRITICAL, WELLNESS_THRESHOLD_GAME_OVER,
    DARK_OVERLAY_LOW_ALPHA, DARK_OVERLAY_CRITICAL_ALPHA,
    WELLNESS_BAR_RECT, WELLNESS_BAR_ID, WELLNESS_BAR_CLASS_ID,
    INITIAL_WELLNESS, MAX_WELLNESS,
    # NEW IMPORTS FOR FLICKER
    FLICKER_THRESHOLD, FLICKER_BASE_ALPHA, FLICKER_MAX_ALPHA_LOW,
    FLICKER_MAX_ALPHA_CRITICAL, FLICKER_SPEED_LOW, FLICKER_SPEED_CRITICAL, MAX_POP_UPS_STAGE_THREE,
    MAX_POP_UPS_STAGE_TWO, POP_UP_CHECK_INTERVAL_SECONDS_STAGE_ONE
)
from game_clock import GameClock
from ui_manager import UIManager
from game_state import GameState

pygame.init()
pygame.display.set_caption('Quick Start')

window_surface = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
background = pygame.Surface((WINDOWS_WIDTH, WINDOWS_HEIGHT))
background.fill(pygame.Color('antiquewhite3'))
game_state = GameState()
ui_manager = UIManager((WINDOWS_WIDTH, WINDOWS_HEIGHT), theme_path="theme.json", game_state_ref=game_state)
def play():
    game_clock_drawer = GameClock(window_surface)
    ui_manager._create_buttons()
    # Define pop-ups for wellness events (can also be in popups2.json if preferred)
    WELLNESS_LOW_POPUP_DEFINITION = {
        "id": "wellness_low_alert",
        "title": "¡Cuidado!",
        "message": "Te sientes cansado y estresado. Deberías tomar un descanso o hacer algo para sentirte mejor.",
        "options": [
            {"label": "Descansar", "consequence": {"wellness_change": 20}},
            {"label": "Seguir", "consequence": {"wellness_change": -10}}
        ]
    }

    WELLNESS_CRITICAL_POPUP_DEFINITION = {
        "id": "wellness_critical_alert",
        "title": "¡ALERTA CRÍTICA!",
        "message": "Tu bienestar es extremadamente bajo. ¡Necesitas actuar ahora o sufrirás las consecuencias!",
        "options": [
            {"label": "Buscar ayuda", "consequence": {"wellness_change": 50}},
            {"label": "Ignorar", "consequence": {"wellness_change": -30}}
        ]
    }

    GAME_OVER_POPUP_DEFINITION = {
        "id": "game_over_final",
        "title": "Fin del Juego",
        "message": "Tu bienestar ha llegado a cero. No pudiste seguir adelante.",
        "options": []
    }


    eye_image = None

    # UIStatusBar instantiation (UNCHANGED)
    wellness_bar = UIStatusBar(
        relative_rect=WELLNESS_BAR_RECT,
        container=None,
        manager=ui_manager.manager,
        object_id=WELLNESS_BAR_ID # Now only uses object_id for specific styling
    )
    # Initialize the status bar using percent_full
    wellness_bar.percent_full = game_state.wellness / MAX_WELLNESS
    # wellness_bar.set_display_number_format('{0:.0f}')

    # wellness_bar.set_display_number_format('{0:.0f}')

    # --- NEW: Flicker timer variable ---
    flicker_timer = 0.0

    clock = pygame.time.Clock()

    is_running = True
    while is_running:
        time_delta = clock.tick(60) / 1000.0
        current_real_time = time.time()

        game_state.update_stage()
        game_state.update_in_game_time(time_delta)
        wellness_bar.percent_full = game_state.wellness / MAX_WELLNESS
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
        # Handle wellness-triggered events
        # wellness_events_to_trigger = game_state.get_wellness_events_to_trigger()
        # for event_id in wellness_events_to_trigger:
        #     if event_id == "wellness_low":
        #         print("TRIGGER: Low Wellness Event!")
        #         ui_manager.popup_manager.create_wellness_event_popup(WELLNESS_LOW_POPUP_DEFINITION,
        #                                                              screen_size=(WINDOWS_WIDTH, WINDOWS_HEIGHT))
        #     elif event_id == "wellness_critical":
        #         print("TRIGGER: Critical Wellness Event!")
        #         for p_info in ui_manager.popup_manager.active_popups[:]:
        #             if p_info['data'].get('id') == WELLNESS_LOW_POPUP_DEFINITION['id']:
        #                 p_info['window'].kill()
        #                 ui_manager.popup_manager.active_popups.remove(p_info)
        #         ui_manager.popup_manager.create_wellness_event_popup(WELLNESS_CRITICAL_POPUP_DEFINITION,
        #                                                              screen_size=(WINDOWS_WIDTH, WINDOWS_HEIGHT))
        #     elif event_id == "game_over":
        #         print("GAME OVER: Wellness reached zero!")
        #         game_over_popup = ui_manager.popup_manager.create_wellness_event_popup(GAME_OVER_POPUP_DEFINITION,
        #                                                                                screen_size=(WINDOWS_WIDTH, WINDOWS_HEIGHT))
        #         if game_over_popup:
        #             game_over_popup["window"].show()
        #             is_running = False


        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            ui_manager.process_event(event)

        # Update UI manager
        ui_manager.update(time_delta)

        # Drawing
        window_surface.blit(background, (0, 0))
        ui_manager.draw(window_surface)
        game_clock_drawer.draw(game_state.in_game_time)

        wellness_bar.redraw()

        # --- Visual Effects based on Wellness ---

        # 1. Static Dark Overlay (UNCHANGED)
        overlay_alpha = 0
        if game_state.wellness <= WELLNESS_THRESHOLD_CRITICAL:
            overlay_alpha = DARK_OVERLAY_CRITICAL_ALPHA
        elif game_state.wellness <= WELLNESS_THRESHOLD_LOW:
            overlay_alpha = DARK_OVERLAY_LOW_ALPHA

        if overlay_alpha > 0:
            dark_overlay = pygame.Surface((WINDOWS_WIDTH, WINDOWS_HEIGHT), pygame.SRCALPHA)
            dark_overlay.fill((0, 0, 0, overlay_alpha))
            window_surface.blit(dark_overlay, (0, 0))

        # 2. Flickering Overlay (NEW)
        if game_state.wellness <= FLICKER_THRESHOLD:
            flicker_timer += time_delta # Increment timer for oscillation

            flicker_max_alpha = 0
            flicker_speed = 0

            if game_state.wellness <= WELLNESS_THRESHOLD_CRITICAL:
                flicker_max_alpha = FLICKER_MAX_ALPHA_CRITICAL
                flicker_speed = FLICKER_SPEED_CRITICAL
            elif game_state.wellness <= FLICKER_THRESHOLD: # Applies for FLICKER_THRESHOLD down to CRITICAL
                flicker_max_alpha = FLICKER_MAX_ALPHA_LOW
                flicker_speed = FLICKER_SPEED_LOW

            # Calculate oscillating alpha value
            # sin wave from -1 to 1, shifted to 0 to 1, scaled by max_alpha, plus base alpha
            flicker_alpha = (math.sin(flicker_timer * flicker_speed) * 0.5 + 0.5) * flicker_max_alpha + FLICKER_BASE_ALPHA
            flicker_alpha = int(max(0, min(255, flicker_alpha))) # Clamp to 0-255 and convert to int

            if flicker_alpha > 0:
                flicker_overlay = pygame.Surface((WINDOWS_WIDTH, WINDOWS_HEIGHT), pygame.SRCALPHA)
                flicker_overlay.fill((0, 0, 0, flicker_alpha)) # Black flicker
                window_surface.blit(flicker_overlay, (0, 0))

        pygame.display.update()

    pygame.quit()

pygame.display.set_caption('Menu')

BG = pygame.image.load('bg/bg.png')
clock = pygame.time.Clock()
is_running = True

PLAY_BUTTON = UIButton(relative_rect=pygame.Rect((275, 275), (200, 70)),
                        anchors={'left':'left',
                                 'right':'right',
                                 'top':'top',
                                 'bottom':'bottom'},
                        text='PLAY',
                       manager=ui_manager.manager)
# QUIT_BUTTON = UIButton(relative_rect=pygame.Rect((199, 345), (30, 10)),
#                        text='QUIT',
#                        manager=ui_manager.manager)
while is_running:
    time_delta = clock.tick(60) / 1000.0
    window_surface.blit(BG, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == PLAY_BUTTON:
                PLAY_BUTTON.kill()
                # QUIT_BUTTON.kill()
                play()
        ui_manager.manager.process_events(event)
        ui_manager.manager.update(time_delta)
    ui_manager.manager.draw_ui(window_surface)
    pygame.display.update()
