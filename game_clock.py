# game_clock.py
import pygame
import math
from game_config import (
    CLOCK_CENTER, CLOCK_RADIUS, HOUR_HAND_LENGTH_RATIO, MINUTE_HAND_LENGTH_RATIO,
    HOUR_HAND_THICKNESS, MINUTE_HAND_THICKNESS, CLOCK_FACE_COLOR, CLOCK_BORDER_COLOR,
    HOUR_HAND_COLOR, MINUTE_HAND_COLOR
)

class GameClock:
    def __init__(self, surface):
        self.surface = surface
        self.center = CLOCK_CENTER
        self.radius = CLOCK_RADIUS

    def draw(self, time_value):
        # Draw clock face
        pygame.draw.circle(self.surface, CLOCK_FACE_COLOR, self.center, self.radius)
        pygame.draw.circle(self.surface, CLOCK_BORDER_COLOR, self.center, self.radius, 2)

        hour = time_value.hour % 12
        minute = time_value.minute

        # Calculate angles for hands (offset by -90 degrees because 0 degrees is usually to the right)
        hour_angle = (360 / 12) * hour + (360 / (12 * 60)) * minute - 90
        minute_angle = (360 / 60) * minute - 90

        # Calculate end points for hour hand
        hour_x = self.center[0] + int(self.radius * HOUR_HAND_LENGTH_RATIO * math.cos(math.radians(hour_angle)))
        hour_y = self.center[1] + int(self.radius * HOUR_HAND_LENGTH_RATIO * math.sin(math.radians(hour_angle)))

        # Calculate end points for minute hand
        minute_x = self.center[0] + int(self.radius * MINUTE_HAND_LENGTH_RATIO * math.cos(math.radians(minute_angle)))
        minute_y = self.center[1] + int(self.radius * MINUTE_HAND_LENGTH_RATIO * math.sin(math.radians(minute_angle)))

        # Draw hands
        pygame.draw.line(self.surface, HOUR_HAND_COLOR, self.center, (hour_x, hour_y), HOUR_HAND_THICKNESS)
        pygame.draw.line(self.surface, MINUTE_HAND_COLOR, self.center, (minute_x, minute_y), MINUTE_HAND_THICKNESS)