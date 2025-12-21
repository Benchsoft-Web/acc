"""
Refactored AFK Reconnect Monitor
Watches for disconnect/reconnect popups and auto-responds
"""

import pytesseract
import time
import keyboard
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import TESSERACT_PATH, BUTTONS_DIR
from windows_manager import RobloxWindowManager
from input_simulator import InputSimulator
from button_detector import ButtonDetector, ButtonActions
import pyautogui

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Setup Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

stop_flag = False

def stop_script():
    global stop_flag
    stop_flag = True
    logger.info("Stop hotkey pressed. Exiting...")

keyboard.add_hotkey('ctrl+shift+p', stop_script)
logger.info("Press Ctrl+Shift+P to stop the script.")


class AFKMonitor:
    """Monitors for disconnect/reconnect events"""
    
    def __init__(self):
        self.window_mgr = RobloxWindowManager()
        self.input = InputSimulator()
        self.detector = ButtonDetector(BUTTONS_DIR)
        self.actions = ButtonActions(self.detector, self.input)
    
    def dismiss_modal_ocr(self) -> bool:
        """Find and dismiss modal using OCR
        
        Returns:
            True if dismissed
        """
        region = self.window_mgr.get_roblox_region()
        if not region:
            return False
        
        screenshot = pyautogui.screenshot(region=region)
        gray = screenshot.convert("L")
        data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
        
        # Look for dismiss button text
        for i, word in enumerate(data["text"]):
            if "dismiss" in word.lower():
                x = data["left"][i] + data["width"][i] // 2 + region[0]
                y = data["top"][i] + data["height"][i] // 2 + region[1]
                self.input.wiggle_and_click(x, y)
                logger.info(f"Dismissed modal at ({x}, {y})")
                return True
        
        return False
    
    def try_reconnect(self) -> bool:
        """Attempt to click reconnect button
        
        Returns:
            True if clicked
        """
        region = self.window_mgr.get_roblox_region()
        if not region:
            return False
        
        # Try to find and click reconnect button
        return self.actions.click_button_if_visible("reconnect", region=region)
    
    def run_monitor(self) -> None:
        """Main monitoring loop - watches for disconnect/reconnect events"""
        global stop_flag
        
        logger.info("Starting AFK Monitor")
        logger.info("This will watch for disconnect/reconnect popups")
        
        consecutive_errors = 0
        max_errors = 5
        
        while not stop_flag:
            try:
                # Ensure Roblox window exists
                if not self.window_mgr.is_roblox_running():
                    logger.warning("Roblox not running, waiting...")
                    time.sleep(5)
                    continue
                
                # Focus window
                self.window_mgr.focus_roblox(start_if_missing=False)
                
                # Try to dismiss any modal
                self.dismiss_modal_ocr()
                
                # Try to reconnect if needed
                self.try_reconnect()
                
                # Check interval
                time.sleep(2)
                consecutive_errors = 0
                
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
                consecutive_errors += 1
                
                if consecutive_errors >= max_errors:
                    logger.error(f"Too many errors ({max_errors}), exiting")
                    break
                
                time.sleep(5)
        
        logger.info("Monitor stopped")


def main():
    """Entry point"""
    monitor = AFKMonitor()
    
    if not monitor.window_mgr.focus_roblox():
        logger.error("Cannot start: Roblox not found")
        print("Roblox must be running. Please start Roblox and try again.")
        return
    
    monitor.run_monitor()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Monitor interrupted by user")
