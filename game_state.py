# game_state.py
import datetime
import time
import pygame
import pygame_gui.elements
from game_config import (
    INITIAL_IN_GAME_TIME
)

class GameState:
    def __init__(self):
        self.in_game_time = INITIAL_IN_GAME_TIME
        self.current_stage = 1
        self.player_state = {} # Stores consequences, e.g., {"reunion_grupo": True}
        self.time_progression_multiplier = 1.0
        self._start_real_time = time.time()
        self._last_popup_check_time = time.time()

    def should_check_for_popup(self, current_real_time, check_interval):
        if current_real_time - self._last_popup_check_time > check_interval:
            self._last_popup_check_time = current_real_time
            return True
        return False
