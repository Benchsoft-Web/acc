"""
Windows management utility module
Handles Roblox window detection, focusing, and region calculation
Eliminates duplication across all scripts
"""

import psutil
import win32gui
import win32process
import win32con
import time
import subprocess
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class RobloxWindowManager:
    """Handles all Roblox window operations"""
    
    @staticmethod
    def get_roblox_pids() -> set:
        """Find all Roblox process IDs"""
        pids = set()
        for proc in psutil.process_iter(['pid', 'exe']):
            try:
                exe_path = proc.info['exe']
                if exe_path and "roblox" in exe_path.lower():
                    pids.add(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return pids
    
    @staticmethod
    def get_roblox_hwnd() -> Optional[int]:
        """Get window handle for Roblox application
        
        Returns:
            Window handle (hwnd) or None if not found
        """
        target_pids = RobloxWindowManager.get_roblox_pids()
        if not target_pids:
            logger.warning("No Roblox process found")
            return None
        
        hwnd_match = None
        def enum_handler(hwnd, _):
            nonlocal hwnd_match
            if not win32gui.IsWindowVisible(hwnd):
                return
            title = win32gui.GetWindowText(hwnd)
            if not title or "roblox" not in title.lower():
                return
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if pid in target_pids:
                    hwnd_match = hwnd
            except Exception:
                pass
        
        win32gui.EnumWindows(enum_handler, None)
        if hwnd_match:
            logger.debug(f"Found Roblox window: {hwnd_match}")
        return hwnd_match
    
    @staticmethod
    def get_roblox_region() -> Optional[Tuple[int, int, int, int]]:
        """Get the window region (left, top, width, height) of Roblox window
        
        Returns:
            (left, top, width, height) or None if window not found
        """
        hwnd = RobloxWindowManager.get_roblox_hwnd()
        if not hwnd:
            logger.error("Cannot get region: Roblox window not found")
            return None
        
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        region = (left, top, right - left, bottom - top)
        logger.debug(f"Roblox region: {region}")
        return region
    
    @staticmethod
    def focus_roblox(start_if_missing: bool = True) -> bool:
        """Focus and maximize the Roblox window
        
        Args:
            start_if_missing: If True, attempt to start Roblox if not running
            
        Returns:
            True if successfully focused, False otherwise
        """
        hwnd = RobloxWindowManager.get_roblox_hwnd()
        
        if not hwnd:
            if start_if_missing:
                logger.info("Roblox not found. Attempting to start...")
                try:
                    subprocess.Popen(["RobloxPlayerBeta.exe"])
                    time.sleep(5)
                    hwnd = RobloxWindowManager.get_roblox_hwnd()
                    if not hwnd:
                        logger.error("Failed to find Roblox after starting")
                        return False
                except Exception as e:
                    logger.error(f"Failed to start Roblox: {e}")
                    return False
            else:
                logger.error("Roblox window not found")
                return False
        
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            time.sleep(0.05)
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.05)
            logger.info("Roblox window focused and maximized")
            return True
        except Exception as e:
            logger.error(f"Failed to focus Roblox: {e}")
            return False
    
    @staticmethod
    def is_roblox_running() -> bool:
        """Check if Roblox is running"""
        return bool(RobloxWindowManager.get_roblox_hwnd())
