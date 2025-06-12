# game_state.py
import datetime
import time
import pygame
import pygame_gui.elements
from game_config import (
    INITIAL_IN_GAME_TIME, REAL_TIME_SECONDS_PER_IN_GAME_SECOND,
    STAGE_ONE_DURATION_SECONDS, STAGE_TWO_DURATION_SECONDS,
    INITIAL_WELLNESS, MIN_WELLNESS, MAX_WELLNESS,
    WELLNESS_DECAY_RATE_PER_SECOND,
    WELLNESS_THRESHOLD_LOW, WELLNESS_THRESHOLD_CRITICAL, WELLNESS_THRESHOLD_GAME_OVER,
    WELLNESS_ACCELERATION_FACTOR_LOW_WELLNESS, WELLNESS_ACCELERATION_FACTOR_CRITICAL_WELLNESS
)

class GameState:
    def __init__(self):
        self.in_game_time = INITIAL_IN_GAME_TIME
        self.current_stage = 1
        self.player_state = {} # Stores consequences, e.g., {"reunion_grupo": True}

        self._start_real_time = time.time()
        self._last_popup_check_time = time.time()
        self.wellness = 100
        self._last_wellness_decay_time = time.time()
        self._wellness_events_triggered = {  # Flags to prevent event spam
            "wellness_low": False,
            "wellness_critical": False,
            "game_over": False
        }

    def update_stage(self):
        # The base elapsed real time
        elapsed_real_time = time.time() - self._start_real_time

        # Apply wellness-based acceleration to "effective" elapsed time
        current_acceleration_factor = 1.0
        if self.wellness <= WELLNESS_THRESHOLD_CRITICAL:
            current_acceleration_factor = WELLNESS_ACCELERATION_FACTOR_CRITICAL_WELLNESS
        elif self.wellness <= WELLNESS_THRESHOLD_LOW:
            current_acceleration_factor = WELLNESS_ACCELERATION_FACTOR_LOW_WELLNESS

        effective_elapsed_time = elapsed_real_time * current_acceleration_factor

        if effective_elapsed_time >= (STAGE_ONE_DURATION_SECONDS + STAGE_TWO_DURATION_SECONDS):
            self.current_stage = 3
        elif effective_elapsed_time >= STAGE_ONE_DURATION_SECONDS:
            self.current_stage = 2
        else:
            self.current_stage = 1

    def update_in_game_time(self, time_delta):
        # The original code had: in_game_time+=datetime.timedelta(seconds=0.25*etapa)
        # Assuming current_stage is equivalent to 'etapa' for this calculation.
        time_progression_multiplier = 1.0
        if self.wellness <= WELLNESS_THRESHOLD_CRITICAL:
            time_progression_multiplier = WELLNESS_ACCELERATION_FACTOR_CRITICAL_WELLNESS
        elif self.wellness <= WELLNESS_THRESHOLD_LOW:
            time_progression_multiplier = WELLNESS_ACCELERATION_FACTOR_LOW_WELLNESS

        self.in_game_time += datetime.timedelta(seconds=time_delta * (
                    1 / REAL_TIME_SECONDS_PER_IN_GAME_SECOND) * self.current_stage * time_progression_multiplier)

        current_time = time.time()
        decay_interval = current_time - self._last_wellness_decay_time
        if decay_interval >= 1.0:  # Decay every real second
            self.adjust_wellness(-WELLNESS_DECAY_RATE_PER_SECOND * decay_interval)
            self._last_wellness_decay_time = current_time

    def should_check_for_popup(self, current_real_time, check_interval):
        if current_real_time - self._last_popup_check_time > check_interval:
            self._last_popup_check_time = current_real_time
            return True
        return False

    def adjust_wellness(self, amount):
        """Adjusts the player's wellness, clamping it between MIN_WELLNESS and MAX_WELLNESS."""
        self.wellness = max(MIN_WELLNESS, min(MAX_WELLNESS, self.wellness + amount))
        # print(f"Wellness adjusted by {amount}. New wellness: {self.wellness}") # For debugging

    def update_player_state(self, consequence_dict):
        """
        Updates the player's state and wellness based on the consequence of a popup choice.
        This is called by PopupManager.
        """
        if consequence_dict:
            # Apply wellness change
            wellness_change = consequence_dict.get("wellness_change", 0)
            if wellness_change != 0: # Only adjust if there's an actual change specified
                self.adjust_wellness(wellness_change)

            # Apply other general state changes (excluding wellness_change key)
            temp_consequence_dict = {k: v for k, v in consequence_dict.items() if k != "wellness_change"}
            if temp_consequence_dict:
                self.player_state.update(temp_consequence_dict)
                print(f"Player state updated: {self.player_state}")

    def get_wellness_events_to_trigger(self):
        """
        Checks wellness thresholds and returns a list of unique event IDs to trigger.
        Ensures events trigger only once per threshold crossing.
        """
        events = []

        # Game Over Condition
        if self.wellness <= WELLNESS_THRESHOLD_GAME_OVER and not self._wellness_events_triggered["game_over"]:
            events.append("game_over")
            self._wellness_events_triggered["game_over"] = True
            self._wellness_events_triggered["wellness_critical"] = True  # Also implies critical/low
            self._wellness_events_triggered["wellness_low"] = True
            return events  # Game over takes precedence

        # Critical Wellness Threshold
        if self.wellness <= WELLNESS_THRESHOLD_CRITICAL and not self._wellness_events_triggered["wellness_critical"]:
            events.append("wellness_critical")
            self._wellness_events_triggered["wellness_critical"] = True
            self._wellness_events_triggered["wellness_low"] = True  # Critical also means low
        elif self.wellness > WELLNESS_THRESHOLD_CRITICAL and self._wellness_events_triggered["wellness_critical"]:
            # Reset critical flag if wellness recovers above critical threshold
            self._wellness_events_triggered["wellness_critical"] = False

        # Low Wellness Threshold
        if self.wellness <= WELLNESS_THRESHOLD_LOW and not self._wellness_events_triggered["wellness_low"]:
            events.append("wellness_low")
            self._wellness_events_triggered["wellness_low"] = True
        elif self.wellness > WELLNESS_THRESHOLD_LOW and self._wellness_events_triggered["wellness_low"]:
            # Reset low flag if wellness recovers above low threshold (and not critical)
            self._wellness_events_triggered["wellness_low"] = False

        return events