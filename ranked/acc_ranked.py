"""
Refactored Ranked Mode Bot
Uses centralized utilities for faster development and less code duplication
"""

import pytesseract
import time
import keyboard
import logging
from PIL import Image
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import TESSERACT_PATH, BUTTONS_DIR, BUTTON_OFFSETS
from windows_manager import RobloxWindowManager
from input_simulator import InputSimulator
from button_detector import ButtonDetector, ButtonActions
import pyautogui

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Setup Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# Global stop flag
stop_flag = False

def stop_script():
    global stop_flag
    stop_flag = True
    logger.info("Stop hotkey pressed. Exiting...")

# Register stop hotkey
keyboard.add_hotkey('ctrl+shift+p', stop_script)
logger.info("Press Ctrl+Shift+P to stop the script.")


class RankedBot:
    """Main ranked mode automation bot"""
    
    def __init__(self):
        self.window_mgr = RobloxWindowManager()
        self.input = InputSimulator()
        self.detector = ButtonDetector(BUTTONS_DIR)
        self.actions = ButtonActions(self.detector, self.input)
    
    def dismiss_modal(self) -> bool:
        """Find and dismiss any modal dialogs via OCR
        
        Returns:
            True if dismissed, False otherwise
        """
        region = self.window_mgr.get_roblox_region()
        if not region:
            logger.error("Cannot get region")
            return False
        
        screenshot = pyautogui.screenshot(region=region)
        gray = screenshot.convert("L")
        data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
        
        for i, word in enumerate(data["text"]):
            if "dismiss" in word.lower():
                x = data["left"][i] + data["width"][i] // 2 + region[0]
                y = data["top"][i] + data["height"][i] // 2 + region[1]
                self.input.wiggle_and_click(x, y)
                logger.info(f"Dismissed modal at ({x}, {y})")
                return True
        
        return False
    
    def click_button_safe(self, button_name: str) -> bool:
        """Safely click a button with error handling
        
        Returns:
            True if clicked, False otherwise
        """
        offset = BUTTON_OFFSETS.get(button_name, (0, 0))
        return self.actions.click_button(button_name, offset=offset)
    
    def run_loop(self) -> None:
        """Main automation loop"""
        global stop_flag
        
        while not stop_flag:
            try:
                # Ensure Roblox is focused
                if not self.window_mgr.is_roblox_running():
                    logger.error("Roblox not running. Attempting to focus...")
                    if not self.window_mgr.focus_roblox():
                        logger.error("Failed to focus Roblox. Retrying in 5s...")
                        time.sleep(5)
                        continue
                
                # Dismiss any popups/modals
                self.dismiss_modal()
                
                # Standard action clicks
                self.click_button_safe("fight")
                self.click_button_safe("ranked")
                self.click_button_safe("refresh")
                
                time.sleep(1)  # Main loop delay
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)
                time.sleep(2)


def main():
    """Entry point"""
    logger.info("Starting Ranked Bot")
    bot = RankedBot()
    
    if not bot.window_mgr.focus_roblox():
        logger.error("Cannot start: Roblox not found")
        return
    
    bot.run_loop()
    logger.info("Bot exited")


if __name__ == "__main__":
    main()
