import pyautogui
import pydirectinput
import pytesseract
from PIL import Image
import psutil
import win32gui
import win32process
import win32con
import time
import keyboard
import os
import random
import math
from pyautogui import ImageNotFoundException

# Path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

stop_flag = False

def stop_script():
    global stop_flag
    stop_flag = True
    print("Stop hotkey pressed. Exiting...")

keyboard.add_hotkey('ctrl+shift+p', stop_script)
print("Press Ctrl+Shift+P to stop the script.")

def get_roblox_hwnd():
    target_pids = set()
    for proc in psutil.process_iter(['pid', 'exe']):
        try:
            exe_path = proc.info['exe']
            if exe_path and exe_path.lower().endswith("robloxplayerbeta.exe"):
                target_pids.add(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if not target_pids:
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
    return hwnd_match

def get_roblox_region():
    hwnd = get_roblox_hwnd()
    if not hwnd:
        return None
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return (left, top, right - left, bottom - top)

def focus_roblox():
    hwnd = get_roblox_hwnd()
    if not hwnd:
        print("RobloxPlayerBeta.exe window not found.")
        return
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        time.sleep(0.1)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.1)
        print("Roblox window maximized and focused.")
    except Exception as e:
        print("Failed to maximize/focus Roblox window:", e)

# --- Smooth, fast human-like movement ---
def human_move(x, y, steps=2):
    start_x, start_y = pydirectinput.position()
    dx = x - start_x
    dy = y - start_y
    for i in range(1, steps+1):
        t = i / steps
        ease = (1 - math.cos(t * math.pi)) / 2  # smooth easing
        move_x = int(start_x + dx * ease)
        move_y = int(start_y + dy * ease)
        pydirectinput.moveTo(move_x, move_y)
        time.sleep(0.001)  # quick, smooth intervals

def wiggle_and_click(x, y):
    human_move(x, y)
    # gentle wiggle
    for _ in range(2):
        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-1, 1)
        pydirectinput.moveRel(offset_x, offset_y)
        time.sleep(random.uniform(0.015, 0.019))
        pydirectinput.moveRel(-offset_x, -offset_y)
    pydirectinput.click()
    # no pause after click

def dismiss_modal():
    region = get_roblox_region()
    if not region:
        return False
    screenshot = pyautogui.screenshot(region=region)
    gray = screenshot.convert("L")
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
    for i, word in enumerate(data["text"]):
        if "dismiss" in word.lower():
            x = data["left"][i] + data["width"][i] // 2 + region[0]
            y = data["top"][i] + data["height"][i] // 2 + region[1]
            wiggle_and_click(x, y)
            print(f"Dismissed modal at ({x}, {y})")
            return True
    return False

def click_fight():
    try:
        if not os.path.exists("fight_button.png"):
            print("Missing template: fight_button.png")
            return False
        location = pyautogui.locateCenterOnScreen("fight_button.png", confidence=0.8)
        if location:
            x, y = location
            wiggle_and_click(x, y)
            print("Clicked Fight button")
            return True
        print("Fight button not found on screen.")
        return False
    except ImageNotFoundException:
        print("Fight button not found (exception).")
        return False

def click_ranked():
    try:
        if not os.path.exists("ranked_button.png"):
            print("Missing template: ranked_button.png")
            return False
        location = pyautogui.locateCenterOnScreen("ranked_button.png", confidence=0.8)
        if location:
            x, y = location
            wiggle_and_click(x, y - 15)
            print("Clicked Ranked button")
            return True
        print("Ranked button not found on screen.")
        return False
    except ImageNotFoundException:
        print("Ranked button not found (exception).")
        return False

def click_refresh():
    try:
        if not os.path.exists("refresh_button.png"):
            print("Missing template: refresh_button.png")
            return False
        location = pyautogui.locateCenterOnScreen("refresh_button.png", confidence=0.8)
        if location:
            x, y = location
            wiggle_and_click(x, y)
            print("Clicked Refresh button")
            return True
        print("Refresh button not found on screen.")
        return False
    except ImageNotFoundException:
        print("Refresh button not found (exception).")
        return False

def click_reconnect():
    try:
        if not os.path.exists("reconnect_button.png"):
            print("Missing template: reconnect_button.png")
            return False
        location = pyautogui.locateCenterOnScreen("reconnect_button.png", confidence=0.9)
        if location:
            x, y = location
            wiggle_and_click(x, y)
            print("Clicked Reconnect button")
            return True
        print("Reconnect button not found on screen.")
        return False
    except ImageNotFoundException:
        print("Reconnect button not found (exception).")
        return False

# --- Main Loop ---
def main_loop():
    global stop_flag
    while not stop_flag:
        focus_roblox()
        dismiss_modal()
        click_reconnect()

if __name__ == "__main__":
    main_loop()