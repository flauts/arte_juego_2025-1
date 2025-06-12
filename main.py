# main.py
import pygame
import pygame_gui
import time
import datetime

from game_config import (
    WINDOWS_WIDTH, WINDOWS_HEIGHT, POP_UP_CHECK_INTERVAL_SECONDS, MAX_POP_UPS_STAGE_ONE
)
from game_clock import GameClock
from ui_manager import UIManager
from game_state import GameState
# popup_handler is imported by ui_manager, so no direct import needed here

pygame.init()
pygame.display.set_caption('Quick Start')

window_surface = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
background = pygame.Surface((WINDOWS_WIDTH, WINDOWS_HEIGHT))
background.fill(pygame.Color('antiquewhite3'))

# Initialize game state first as others depend on it
game_state = GameState()
# Initialize UIManager, passing game_state reference for pop-up logic
ui_manager = UIManager((WINDOWS_WIDTH, WINDOWS_HEIGHT), theme_path="theme.json", game_state_ref=game_state)
game_clock_drawer = GameClock(window_surface) # GameClock also uses the surface

clock = pygame.time.Clock()

is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0 # Time since last frame in seconds
    current_real_time = time.time() # Current real-world time

    # Update game state (stage and in-game time progression)
    game_state.update_stage()
    game_state.update_in_game_time(time_delta)

    # Logic to trigger pop-ups based on game time and stage
    if game_state.should_check_for_popup(current_real_time, POP_UP_CHECK_INTERVAL_SECONDS):
        # Only create pop-ups for stage 1 and if the limit hasn't been reached
        if game_state.current_stage == 1 and len(ui_manager.popup_manager.active_popups) < MAX_POP_UPS_STAGE_ONE:
            # Request a new popup from the PopupManager, passing current screen dimensions
            new_popup_info = ui_manager.popup_manager.create_popup_for_stage(game_state.current_stage,
                                                                              screen_size=(WINDOWS_WIDTH, WINDOWS_HEIGHT))
            if new_popup_info:
                new_popup_info["window"].show() # Make the newly created popup visible
        # You can extend this with logic for stage 2 and 3 pop-ups as needed

    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False # Set flag to exit the game loop

        # Pass all events to the UIManager for processing UI interactions
        ui_manager.process_event(event)

    # Update UI manager (updates elements, animations, etc.)
    ui_manager.update(time_delta)

    # Drawing operations
    window_surface.blit(background, (0, 0)) # Draw the background
    ui_manager.draw(window_surface) # Draw all UI elements (buttons, windows, popups)
    game_clock_drawer.draw(game_state.in_game_time) # Draw the analog clock

    pygame.display.update() # Update the entire screen

pygame.quit() # Uninitialize Pygame modules