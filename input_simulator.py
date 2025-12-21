"""
Input simulation utility module
Handles human-like mouse and keyboard input
"""

import pydirectinput
import time
import random
import math
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class InputSimulator:
    """Handles human-like input simulation"""
    
    def __init__(self, move_steps: int = 3, 
                 move_min_delay: float = 0.0012,
                 move_max_delay: float = 0.0015,
                 wiggle_iterations: int = 2,
                 wiggle_min_offset: Tuple[int, int] = (-2, -1),
                 wiggle_max_offset: Tuple[int, int] = (2, 1),
                 wiggle_min_delay: float = 0.015,
                 wiggle_max_delay: float = 0.019):
        """Initialize input simulator with behavior parameters
        
        Args:
            move_steps: Number of steps for eased movement
            move_min_delay: Minimum delay between move steps
            move_max_delay: Maximum delay between move steps
            wiggle_iterations: How many times to wiggle before clicking
            wiggle_min_offset: Min (x, y) offset for wiggle
            wiggle_max_offset: Max (x, y) offset for wiggle
            wiggle_min_delay: Min wiggle step delay
            wiggle_max_delay: Max wiggle step delay
        """
        self.move_steps = move_steps
        self.move_min_delay = move_min_delay
        self.move_max_delay = move_max_delay
        self.wiggle_iterations = wiggle_iterations
        self.wiggle_min_offset = wiggle_min_offset
        self.wiggle_max_offset = wiggle_max_offset
        self.wiggle_min_delay = wiggle_min_delay
        self.wiggle_max_delay = wiggle_max_delay
    
    def human_move(self, x: int, y: int, steps: int = None) -> None:
        """Move mouse with cosine easing (smooth, human-like)
        
        Args:
            x, y: Target screen coordinates
            steps: Override default steps for this movement
        """
        steps = steps or self.move_steps
        start_x, start_y = pydirectinput.position()
        dx = x - start_x
        dy = y - start_y
        
        for i in range(1, steps + 1):
            t = i / steps
            ease = (1 - math.cos(t * math.pi)) / 2  # Cosine easing
            move_x = int(start_x + dx * ease)
            move_y = int(start_y + dy * ease)
            pydirectinput.moveTo(move_x, move_y)
            time.sleep(random.uniform(self.move_min_delay, self.move_max_delay))
        
        logger.debug(f"Moved to ({x}, {y})")
    
    def wiggle_and_click(self, x: int, y: int, clicks: int = 1) -> None:
        """Move to location, wiggle slightly, then click (avoids bot detection)
        
        Args:
            x, y: Click coordinates
            clicks: Number of clicks
        """
        self.human_move(x, y)
        
        # Gentle wiggle
        for _ in range(self.wiggle_iterations):
            offset_x = random.randint(self.wiggle_min_offset[0], self.wiggle_max_offset[0])
            offset_y = random.randint(self.wiggle_min_offset[1], self.wiggle_max_offset[1])
            pydirectinput.moveRel(offset_x, offset_y)
            time.sleep(random.uniform(self.wiggle_min_delay, self.wiggle_max_delay))
            pydirectinput.moveRel(-offset_x, -offset_y)
        
        pydirectinput.click(clicks=clicks)
        logger.debug(f"Clicked at ({x}, {y}) × {clicks}")
    
    def press_key(self, key: str, duration: float = 0.1) -> None:
        """Press and hold a key
        
        Args:
            key: Key name (e.g., 'w', 'space', 'enter')
            duration: How long to hold the key
        """
        pydirectinput.keyDown(key)
        time.sleep(duration + random.uniform(-0.05, 0.05))
        pydirectinput.keyUp(key)
        logger.debug(f"Pressed {key} for {duration}s")
    
    def drag(self, x1: int, y1: int, x2: int, y2: int, duration: float = 0.3) -> None:
        """Drag from one point to another
        
        Args:
            x1, y1: Starting coordinates
            x2, y2: Ending coordinates
            duration: Duration of drag
        """
        self.human_move(x1, y1)
        pydirectinput.mouseDown()
        time.sleep(0.05)
        
        start_time = time.time()
        while time.time() - start_time < duration:
            progress = (time.time() - start_time) / duration
            ease = (1 - math.cos(progress * math.pi)) / 2
            current_x = int(x1 + (x2 - x1) * ease)
            current_y = int(y1 + (y2 - y1) * ease)
            pydirectinput.moveTo(current_x, current_y)
            time.sleep(0.01)
        
        pydirectinput.moveTo(x2, y2)
        time.sleep(0.05)
        pydirectinput.mouseUp()
        logger.debug(f"Dragged from ({x1}, {y1}) to ({x2}, {y2})")
