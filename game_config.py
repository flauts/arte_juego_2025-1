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
POP_UP_CHECK_INTERVAL_SECONDS_STAGE_ONE = 15 # How often to check for new pop-ups (in real seconds)
POP_UP_CHECK_INTERVAL_SECONDS_STAGE_TWO = 5 # How often to check for new pop-ups (in real seconds)
POP_UP_CHECK_INTERVAL_SECONDS_STAGE_THREE = 1 # How often to check for new pop-ups (in real seconds)
MAX_POP_UPS_STAGE_ONE = 1 # Max pop-ups displayed at once in stage 1
MAX_POP_UPS_STAGE_TWO = 3
MAX_POP_UPS_STAGE_THREE = 10

# UI element IDs
CHAT_ICON_ID = '@chat_icon'
CANVAS_ICON_ID = '@canvas_icon'
ICON_CLASS_ID = '#icon'
WELLNESS_BAR_ID = '@wellness_bar' # ID for the specific wellness bar instance
WELLNESS_BAR_CLASS_ID = '#wellness_bar' # Class ID for styling UIStatusBar elements

# Wellness Bar Settings
MIN_WELLNESS = 0
MAX_WELLNESS = 200
INITIAL_WELLNESS = MAX_WELLNESS
WELLNESS_BAR_RECT = pygame.Rect((10, 10), (200, 25)) # Position and size

# Wellness Decay and Progression Acceleration
WELLNESS_DECAY_RATE_PER_SECOND = 0.2 # How much wellness passively decays per real second
WELLNESS_ACCELERATION_FACTOR_LOW_WELLNESS = 1.5 # Time accelerates 1.5x if wellness is low
WELLNESS_ACCELERATION_FACTOR_CRITICAL_WELLNESS = 2.5 # Time accelerates 2.5x if wellness is critical

# Wellness Event Thresholds and associated event names (for popups/visuals)
WELLNESS_THRESHOLD_LOW = 40       # Trigger "wellness_low" event
WELLNESS_THRESHOLD_CRITICAL = 15  # Trigger "wellness_critical" event
WELLNESS_THRESHOLD_GAME_OVER = 0  # Game over if wellness hits this

# Visual Effects for Wellness (Static Dark Overlay)
DARK_OVERLAY_LOW_ALPHA = 80   # Alpha (0-255) for low wellness overlay
DARK_OVERLAY_CRITICAL_ALPHA = 150 # Alpha for critical wellness overlay

# --- NEW: Flickering Effect Parameters ---
FLICKER_THRESHOLD = 35 # Wellness level below which flickering starts
FLICKER_BASE_ALPHA = 20 # Minimum alpha for flicker when active
FLICKER_MAX_ALPHA_LOW = 80 # Max additional alpha for flicker when wellness is low
FLICKER_MAX_ALPHA_CRITICAL = 150 # Max additional alpha for flicker when wellness is critical
FLICKER_SPEED_LOW = 15.0 # Speed of flicker oscillation for low wellness (higher = faster)
FLICKER_SPEED_CRITICAL = 30.0 # Speed of flicker oscillation for critical wellness