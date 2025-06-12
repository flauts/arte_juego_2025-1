# game_state.py
import datetime
import time
from game_config import (
    INITIAL_IN_GAME_TIME, REAL_TIME_SECONDS_PER_IN_GAME_SECOND,
    STAGE_ONE_DURATION_SECONDS, STAGE_TWO_DURATION_SECONDS
)

class GameState:
    def __init__(self):
        self.in_game_time = INITIAL_IN_GAME_TIME
        self.current_stage = 1
        self.player_state = {} # Stores consequences, e.g., {"reunion_grupo": True}

        self._start_real_time = time.time()
        self._last_popup_check_time = time.time()

    def update_stage(self):
        elapsed_real_time = time.time() - self._start_real_time
        if elapsed_real_time >= (STAGE_ONE_DURATION_SECONDS + STAGE_TWO_DURATION_SECONDS):
            self.current_stage = 3
        elif elapsed_real_time >= STAGE_ONE_DURATION_SECONDS:
            self.current_stage = 2
        else:
            self.current_stage = 1

    def update_in_game_time(self, time_delta):
        # The original code had: in_game_time+=datetime.timedelta(seconds=0.25*etapa)
        # Assuming current_stage is equivalent to 'etapa' for this calculation.
        self.in_game_time += datetime.timedelta(seconds=time_delta * (1/REAL_TIME_SECONDS_PER_IN_GAME_SECOND) * self.current_stage)

    def should_check_for_popup(self, current_real_time, check_interval):
        if current_real_time - self._last_popup_check_time > check_interval:
            self._last_popup_check_time = current_real_time
            return True
        return False

    def update_player_state(self, consequence_dict):
        """Updates the player's state based on the consequence of a popup choice."""
        if consequence_dict:
            self.player_state.update(consequence_dict)
            print(f"Player state updated: {self.player_state}")