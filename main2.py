# main.py
import pygame
import pygame_gui
import time
import datetime

from game_config import (
    WINDOWS_WIDTH, WINDOWS_HEIGHT, CLOCK_CENTER, CLOCK_RADIUS, POP_UP_CHECK_INTERVAL_SECONDS,
    MAX_POP_UPS_STAGE_ONE
)
from game_clock import GameClock
from ui_manager import UIManager
from game_state import GameState
from popup_handler import PopupManager # Import PopupManager directly if needed for game logic beyond UI handling

pygame.init()
pygame.display.set_caption('Quick Start')

window_surface = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
background = pygame.Surface((WINDOWS_WIDTH, WINDOWS_HEIGHT))
background.fill(pygame.Color('antiquewhite3'))

# Initialize managers and game state
ui_manager = UIManager((WINDOWS_WIDTH, WINDOWS_HEIGHT), theme_path="theme.json")
game_clock_drawer = GameClock(window_surface)
game_state = GameState()

clock = pygame.time.Clock()

is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0
    current_real_time = time.time()

    # Update game state (stage, in-game time)
    game_state.update_stage()
    game_state.update_in_game_time(time_delta)

    # Handle pop-up generation
    if game_state.should_check_for_popup(current_real_time, POP_UP_CHECK_INTERVAL_SECONDS):
        if game_state.current_stage == 1 and len(ui_manager.popup_manager.active_popups) < MAX_POP_UPS_STAGE_ONE:
            new_popup = ui_manager.popup_manager.create_popup_from_stage(game_state.current_stage, game_state.player_state)
            if new_popup:
                new_popup["window"].show()
        # You can add logic for stage 2 and 3 pop-ups here

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # Process UI events (buttons, window closes)
        if ui_manager.process_event(event): # If a popup button was handled, it may affect game state
            # Here, you would check the consequence of the popup button press
            # For example, if PopupManager.handle_popup_button_press returned the consequence:
            # game_state.update_player_choice(popup_id, consequence)
            pass

    # Update UI manager
    ui_manager.update(time_delta)

    # Drawing
    window_surface.blit(background, (0, 0))
    ui_manager.draw(window_surface) # Draw all UI elements
    game_clock_drawer.draw(game_state.in_game_time) # Draw the clock

    pygame.display.update()

pygame.quit()