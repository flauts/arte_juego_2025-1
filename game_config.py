# game_config.py
import pygame
import datetime

# Window dimensions
WINDOWS_WIDTH = 800
WINDOWS_HEIGHT = 600

# Clock settings
CLOCK_CENTER = (750, 100)
CLOCK_RADIUS = 50
HOUR_HAND_LENGTH_RATIO = 0.5
MINUTE_HAND_LENGTH_RATIO = 0.8
HOUR_HAND_THICKNESS = 4
MINUTE_HAND_THICKNESS = 2
CLOCK_FACE_COLOR = pygame.Color("antiquewhite")
CLOCK_BORDER_COLOR = pygame.Color("black")
HOUR_HAND_COLOR = pygame.Color("black")
MINUTE_HAND_COLOR = pygame.Color("gray")

# Game time settings
INITIAL_IN_GAME_TIME = datetime.datetime(2024, 1, 1, 8, 0) # Starts at 08:00
REAL_TIME_SECONDS_PER_IN_GAME_SECOND = 0.25 # How fast in-game time progresses
STAGE_ONE_DURATION_SECONDS = 60
STAGE_TWO_DURATION_SECONDS = 180 - STAGE_ONE_DURATION_SECONDS # Total 180s for stage 3, so 120s for stage 2

# Pop-up message timing
POP_UP_CHECK_INTERVAL_SECONDS = 5 # How often to check for new pop-ups (in real seconds)
MAX_POP_UPS_STAGE_ONE = 2 # Max pop-ups displayed at once in stage 1

# UI element IDs
CHAT_ICON_ID = '@chat_icon'
CANVAS_ICON_ID = '@canvas_icon'
ICON_CLASS_ID = '#icon'