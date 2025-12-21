# Roblox Automation Scripts

Computer vision-based Roblox game automation using image recognition (pyautogui), OCR (Tesseract), and human-like input simulation (pydirectinput) on Windows.

## Quick Start (2 Minutes)

```bash
# 1. Automated setup (installs everything)
python setup.py

# 2. Create button templates
# Take PNG screenshots of game buttons → save to buttons/ directory
# (See "Button Templates" section below)

# 3. Run bot from root directory
python ranked/acc_ranked.py
# or
python afk_reconnect/afk_monitor.py

# Stop anytime: Ctrl+Shift+P
```

**Important**: Always run scripts from the **root `acc/` directory**, not from subdirectories.

## What's Included

### Core Modules
- **`vision_module.py`** - Screen capture, image detection, OCR text extraction
- **`reaction_handler.py`** - Action queueing system for coordinated input
- **`example_bot.py`** - Template showing full integration

### Refactored Utilities (New)
- **`config.py`** - Centralized configuration (paths, timeouts, button templates)
- **`windows_manager.py`** - Roblox window detection & focusing (eliminates 67 lines duplication)
- **`input_simulator.py`** - Human-like mouse/keyboard input with configurable easing
- **`button_detector.py`** - Button detection with caching support

### Bot Scripts
- **`ranked/acc_ranked_refactored.py`** ⭐ - Ranked mode automation (new, 104 lines)
- **`ranked/acc_ranked.py`** - Original ranked mode (317 lines, still works)
- **`afk_reconnect/afk_monitor_refactored.py`** ⭐ - AFK disconnect monitoring (new, 80 lines)
- **`afk_reconnect/reconnect.py`** - Original reconnect monitor (197 lines, still works)
- **`dungeon_navigation.py`** - Dungeon navigation automation

## Button Templates

Create PNG screenshots of buttons and save to `buttons/` directory:

```
buttons/
├── fight.png
├── ranked.png
├── refresh.png
├── reconnect.png
├── enter_dungeon.png
└── leave_dungeon.png
```

### How to Create Templates

1. Launch Roblox, navigate to button location
2. Use Windows Snipping Tool (`Win+Shift+S`) to capture button
3. Crop to button only (avoid extra UI)
4. Save as PNG with the names above (without "_button" suffix)
5. Place in `buttons/` directory

**Tips:**
- Capture at same resolution you'll run bot at
- Ensure clean contrast and lighting
- Buttons must be fully visible, unobstructed
- Button detection searches full screen (no region constraint)
- If detection fails, lower confidence in `config.py` (try 0.7-0.8)
- If UI changes, regenerate templates

**Button Naming Convention:**
- Use simple names without "_button" suffix: `fight.png`, not `fight_button.png`
- Names must match exactly (case-sensitive) what's in `config.py`'s `BUTTON_TEMPLATES` dict

## Configuration

All settings in `config.py`:

```python
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
BUTTONS_DIR = Path(__file__).parent / "buttons"

# Detection
IMAGE_CONFIDENCE = 0.8  # Threshold for image matching

# Input behavior
HUMAN_MOVE_STEPS = 3  # Smoother with higher values
WIGGLE_ITERATIONS = 2  # Subtle wiggle before click
HUMAN_MOVE_MIN_DELAY = 0.0012
HUMAN_MOVE_MAX_DELAY = 0.0015

# Timing
ROBLOX_STARTUP_WAIT = 5  # Seconds to wait on startup
DEFAULT_ACTION_DELAY = 0.1  # Delay between actions
```

**To adjust behavior:** Edit values, restart bot.

## Architecture

### Critical Patterns

**1. Window Detection & Focus**
```python
from windows_manager import RobloxWindowManager
mgr = RobloxWindowManager()
mgr.focus_roblox()  # Maximize and focus window
region = mgr.get_roblox_region()  # Get (left, top, width, height)
```

**2. Vision Detection Loop**
```python
vision = VisionModule(region)
while not stop_flag:
    screenshot = vision.capture_screen()
    text = vision.extract_text()
    if "play" in text.lower():
        handler.click(x, y)
```

**3. Human-Like Input**
```python
from input_simulator import InputSimulator
input_sim = InputSimulator()
input_sim.human_move(x, y)  # Smooth easing
input_sim.wiggle_and_click(x, y)  # Anti-bot behavior
```

**4. Button Detection**
```python
from button_detector import ButtonDetector, ButtonActions
actions = ButtonActions(detector, input_sim)
actions.click_button("fight", region=region)  # One-liner
actions.click_button("ranked", region=region, offset=(0, -15))  # With offset
```

### Project Structure

```
acc/
├── setup.py                       # Run once: python setup.py
├── config.py                      # ⭐ All configuration here
├── windows_manager.py             # Window operations (DRY)
├── input_simulator.py             # Human-like input (DRY)
├── button_detector.py             # Button detection (DRY)
├── vision_module.py               # Screen capture & OCR
├── reaction_handler.py            # Action queueing
├── example_bot.py                 # Integration example
├── dungeon_navigation.py          # Dungeon bot
│
├── buttons/                       # ⭐ Put button templates here
│   ├── fight_button.png
│   ├── ranked_button.png
│   └── ...
│
├── ranked/
│   ├── acc_ranked_refactored.py   # ⭐ Recommended
│   └── acc_ranked.py              # Original
│
├── afk_reconnect/
│   ├── afk_monitor_refactored.py  # ⭐ Recommended
│   └── reconnect.py               # Original
│
└── .github/
    └── copilot-instructions.md    # AI agent guide
```

## Troubleshooting

**"Roblox window not found"**
- Ensure Roblox is running
- Maximize the Roblox window
- Script will auto-focus it

**"Button not found"**
- Verify template exists: `buttons/fight_button.png`
- Check logging output for coordinates
- Try lower confidence: `config.py` → `IMAGE_CONFIDENCE = 0.7`
- Retake screenshot if game UI updated

**"Tesseract not found"**
- Verify installed at: `C:\Program Files\Tesseract-OCR\`
- If elsewhere, update `TESSERACT_PATH` in `config.py`

**"Script runs but doesn't click"**
- Verify button template matches game UI exactly
- Check detailed logging: Add to script top:
  ```python
  import logging
  logging.basicConfig(level=logging.DEBUG)
  ```
- Verify button templates in `buttons/` directory

## Dependencies

| Package | Purpose | Notes |
|---------|---------|-------|
| pyautogui | Screen capture, image detection | Use with confidence 0.7-0.9 |
| pydirectinput | Input simulation | More reliable than pyautogui for input |
| pytesseract | OCR text extraction | Requires Tesseract binary |
| pillow | Image processing | For screenshot manipulation |
| psutil | Process enumeration | For Roblox window detection |
| pywin32 | Windows API | For window focusing |
| keyboard | Global hotkey | For Ctrl+Shift+P stop binding |

**Installation:** `python setup.py` (automated) or `pip install [packages]` (manual)

## Usage Examples

### Ranked Mode Automation

```bash
cd ranked
python acc_ranked_refactored.py
```

Automatically:
- Detects buttons (fight, ranked, refresh)
- Handles disconnect/reconnect
- Monitors wave progression
- Navigates dungeons

### AFK Reconnect Monitor

```bash
cd afk_reconnect
python afk_monitor_refactored.py
```

Watches for:
- Disconnect popups
- Reconnect prompts
- Dismisses modals
- Keeps session alive

### Create Custom Bot

```python
from windows_manager import RobloxWindowManager
from input_simulator import InputSimulator
from button_detector import ButtonDetector, ButtonActions
from config import BUTTONS_DIR
import time
import keyboard

stop_flag = False
def stop_script():
    global stop_flag
    stop_flag = True
keyboard.add_hotkey('ctrl+shift+p', stop_script)

# Setup
window_mgr = RobloxWindowManager()
input_sim = InputSimulator()
actions = ButtonActions(
    ButtonDetector(BUTTONS_DIR),
    input_sim
)

# Main loop
while not stop_flag:
    window_mgr.focus_roblox()
    region = window_mgr.get_roblox_region()
    actions.click_button("fight", region=region)
    time.sleep(1)
```

## Key Differences: Original vs Refactored

| Aspect | Original | Refactored |
|--------|----------|-----------|
| Bot size | 317 lines | 104 lines |
| Code duplication | Yes | No |
| Configuration | Scattered | Centralized |
| Setup time | 15-30 min | 2 min |
| Easy to extend | Hard | Easy |
| New features | Copy/paste code | Use utilities |

**All original scripts still work.** Refactored versions are opt-in and recommended.

## Code Standards (For Contributors)

**Type Hints**
```python
def click_button(self, button_name: str, region: Optional[Tuple[int, int, int, int]] = None) -> bool:
```

**Logging (not print)**
```python
import logging
logger = logging.getLogger(__name__)
logger.info("User-facing message")
logger.debug("Developer trace")
logger.error("Error occurred", exc_info=True)
```

**Docstrings**
```python
def find_image(self, path: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
    """Find image on screen.
    
    Args:
        path: Path to template image
        confidence: Match threshold (0.0-1.0)
        
    Returns:
        (x, y) center or None if not found
    """
```

**Error Handling**
```python
try:
    location = detector.find_button("fight")
except FileNotFoundError:
    logger.error("Template missing")
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
```

## Performance Tips

- **Caching**: ButtonDetector caches locations → faster repeated clicks
- **Region search**: Always pass region to avoid full-screen search
- **Delays**: Game is slow to respond → add `time.sleep()` between actions
- **Confidence**: Start at 0.8, lower to 0.7 if misses

## For AI Agents / Copilot

See `.github/copilot-instructions.md` for detailed architecture, patterns, and conventions.

**Key patterns:**
1. Always `focus_roblox()` before detection
2. Use `InputSimulator` for all input (human-like)
3. Queue actions via ReactionHandler
4. Log all significant operations
5. Handle missing Roblox window gracefully

## Backward Compatibility

✅ 100% backward compatible
- Original scripts untouched
- New utilities are optional
- Can mix old and new approaches
- Gradual migration path available

## Support

**Quick help:**
- Button detection: Edit `config.py` → lower `IMAGE_CONFIDENCE`
- Behavior tuning: Modify `config.py` settings
- New feature: Use utilities in `windows_manager.py`, `input_simulator.py`, `button_detector.py`
- Debugging: Enable logging with `logging.basicConfig(level=logging.DEBUG)`

---

**Status**: ✅ Production-ready | **Last Updated**: December 2025
   cd "c:\Users\justi\Desktop\roblox_scripts\acc\ranked"
   ```
3. Run the script:
   ```
   python acc_ranked.py
   ```

## 5. Controls

- The script will start automating clicks on detected buttons.
- Press `Ctrl+Shift+P` to stop the script at any time.

## Troubleshooting

- If the script can't find Roblox, ensure `RobloxPlayerBeta.exe` is running.
- If image recognition fails, verify the PNG files are in the correct directory and match the in-game buttons closely.
- For OCR issues, check that Tesseract is installed correctly and the path is accurate.
- The script maximizes and focuses the Roblox window automatically.

## Notes

- This script uses `pydirectinput` for mouse control, which may require running as administrator if it doesn't work initially.
- Adjust confidence levels in the image matching functions if buttons aren't being detected reliably.
- The `human_move` function simulates natural mouse movement to avoid detection.
