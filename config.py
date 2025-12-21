"""
Configuration file for Roblox automation scripts
Centralized settings for paths, timeouts, and behavior parameters
"""

import os
from pathlib import Path

# ============ PATHS ============
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
PROJECT_ROOT = Path(__file__).parent
BUTTONS_DIR = PROJECT_ROOT / "buttons"

# ============ DETECTION ============
IMAGE_CONFIDENCE = 0.8  # Default confidence for image matching (0.7-0.9)
OCR_LANG = "eng"  # Tesseract language code

# ============ INPUT BEHAVIOR ============
HUMAN_MOVE_STEPS = 3  # Easing steps for mouse movement
HUMAN_MOVE_MIN_DELAY = 0.0012  # Min interval between movement steps
HUMAN_MOVE_MAX_DELAY = 0.0015  # Max interval between movement steps
WIGGLE_ITERATIONS = 2  # How many times to wiggle before clicking
WIGGLE_MIN_OFFSET = (-2, -1)  # (x, y) min offset
WIGGLE_MAX_OFFSET = (2, 1)  # (x, y) max offset
WIGGLE_MIN_DELAY = 0.015
WIGGLE_MAX_DELAY = 0.019

# ============ TIMING ============
FOCUS_DELAY = 0.1  # Delay after focusing window
ROBLOX_STARTUP_WAIT = 5  # Seconds to wait for Roblox to start
DEFAULT_ACTION_DELAY = 0.1  # Delay after actions

# ============ BUTTON TEMPLATES ============
# Define all button templates here
BUTTON_TEMPLATES = {
    "fight": "fight.png",
    "ranked": "ranked.png",
    "refresh": "refresh.png",
    "reconnect": "reconnect.png",
    "enter_dungeon": "enter_dungeon.png",
    "leave_dungeon": "leave_dungeon.png",
}

# Button-specific coordinates adjustments (for offset clicks if needed)
BUTTON_OFFSETS = {
    "ranked": (0, -15),  # Click 15px above center
}

def get_button_path(button_name: str) -> str:
    """Get full path to button template"""
    if button_name not in BUTTON_TEMPLATES:
        raise ValueError(f"Unknown button: {button_name}")
    return str(BUTTONS_DIR / BUTTON_TEMPLATES[button_name])

def get_button_path_safe(button_name: str) -> str:
    """Get button path if it exists, else return None"""
    path = get_button_path(button_name)
    return path if os.path.exists(path) else None
