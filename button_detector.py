"""
Button detection and clicking utility
Simplifies button detection with configuration-driven approach
"""

import pyautogui
import os
import logging
from typing import Optional, Tuple, Callable
from pathlib import Path
from PIL import Image

logger = logging.getLogger(__name__)


class ButtonDetector:
    """Handles image-based button detection and clicking"""
    
    def __init__(self, buttons_dir: Path, confidence: float = 0.8):
        """Initialize button detector
        
        Args:
            buttons_dir: Directory containing button PNG templates
            confidence: Default confidence threshold for detection
        """
        self.buttons_dir = Path(buttons_dir)
        self.confidence = confidence
        self.cache = {}  # Cache button locations
    
    def find_button(self, button_name: str, region: Optional[Tuple[int, int, int, int]] = None,
                   confidence: Optional[float] = None, use_cache: bool = False) -> Optional[Tuple[int, int]]:
        """Find button on screen by name
        
        Args:
            button_name: Name of button (e.g., "fight", "ranked")
            region: Optional region to search (left, top, width, height)
            confidence: Override default confidence
            use_cache: Use cached location if available
            
        Returns:
            (x, y) center coordinates or None
        """
        # Check cache
        if use_cache and button_name in self.cache:
            logger.debug(f"Using cached location for {button_name}")
            return self.cache[button_name]
        
        button_path = self.buttons_dir / f"{button_name}.png"
        if not button_path.exists():
            logger.warning(f"Button template not found: {button_path}")
            return None
        
        try:
            conf = confidence or self.confidence
            button_img = Image.open(button_path)
            img_width, img_height = button_img.size
            logger.debug(f"Button image '{button_name}' size: {img_width}x{img_height}px")
            
            # Don't use region parameter - pyautogui has issues with it
            # Search full screen instead for more reliable detection
            location = pyautogui.locateCenterOnScreen(
                str(button_path),
                confidence=conf
            )
            if location:
                self.cache[button_name] = location
                logger.info(f"Found {button_name} at {location}")
                return location
            else:
                logger.debug(f"{button_name} not visible on screen")
                return None
        except Exception as e:
            logger.error(f"Error detecting {button_name}: {e}")
            return None
    
    def clear_cache(self, button_name: Optional[str] = None) -> None:
        """Clear cached button locations
        
        Args:
            button_name: Clear specific button, or all if None
        """
        if button_name:
            self.cache.pop(button_name, None)
            logger.debug(f"Cleared cache for {button_name}")
        else:
            self.cache.clear()
            logger.debug("Cleared all button cache")


class ButtonActions:
    """High-level button action interface"""
    
    def __init__(self, detector: ButtonDetector, input_simulator):
        """Initialize button actions
        
        Args:
            detector: ButtonDetector instance
            input_simulator: InputSimulator instance
        """
        self.detector = detector
        self.input = input_simulator
    
    def click_button(self, button_name: str, region: Optional[Tuple[int, int, int, int]] = None,
                    offset: Tuple[int, int] = (0, 0), confidence: Optional[float] = None) -> bool:
        """Find and click a button
        
        Args:
            button_name: Button name
            region: Search region
            offset: Coordinate offset from button center
            confidence: Detection confidence
            
        Returns:
            True if clicked, False if not found
        """
        location = self.detector.find_button(button_name, region, confidence)
        if not location:
            logger.warning(f"Could not find button: {button_name}")
            return False
        
        x = location[0] + offset[0]
        y = location[1] + offset[1]
        self.input.wiggle_and_click(x, y)
        logger.info(f"Clicked {button_name}")
        return True
    
    def click_button_if_visible(self, button_name: str, region: Optional[Tuple[int, int, int, int]] = None,
                               offset: Tuple[int, int] = (0, 0)) -> bool:
        """Click button only if it's visible (doesn't log error if missing)
        
        Args:
            button_name: Button name
            region: Search region
            offset: Coordinate offset
            
        Returns:
            True if clicked, False otherwise
        """
        location = self.detector.find_button(button_name, region)
        if not location:
            return False
        
        x = location[0] + offset[0]
        y = location[1] + offset[1]
        self.input.wiggle_and_click(x, y)
        return True
