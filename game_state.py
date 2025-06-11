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
        self.player_state = {} # e.g., {"reunion_grupo": None, "leer_clase": None}

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
        # Adjust time_delta based on stage if needed, or use a fixed rate
        self.in_game_time += datetime.timedelta(seconds=time_delta * (1/REAL_TIME_SECONDS_PER_IN_GAME_SECOND) * self.current_stage)

    def should_check_for_popup(self, current_real_time, check_interval):
        if current_real_time - self._last_popup_check_time > check_interval:
            self._last_popup_check_time = current_real_time
            return True
        return False

    def update_player_choice(self, popup_id, choice_consequence):
        # This method would apply the consequences of player choices
        # For example:
        # self.player_state[popup_id] = choice_consequence
        print(f"Player chose for {popup_id}: {choice_consequence}")