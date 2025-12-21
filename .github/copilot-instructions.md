# Copilot Instructions for Roblox Automation Scripts

## Project Overview

This is a suite of **Roblox game automation scripts** that use computer vision (image recognition + OCR) and input simulation to automate gameplay tasks on Windows. Core patterns: visual detection → reaction queue → human-like input execution.

### Key Modules

- **`vision_module.py`**: Captures screen regions, detects images via `pyautogui`, extracts text via Tesseract OCR
- **`reaction_handler.py`**: Queues actions (clicks, drags, keys) triggered by visual detection; uses `pydirectinput` for input
- **`example_bot.py`**: Template showing how to combine VisionModule + ReactionHandler + text/image triggers
- **`dungeon_navigation.py`**: Full bot for navigating dungeons, uses reactive loop polling for "play" text
- **`ranked/acc_ranked.py`**: Ranked mode automation with button detection and coordinate-based navigation
- **`afk_reconnect/reconnect.py`**: Monitors for disconnect/reconnect popups and auto-closes them

## Critical Architecture Patterns

### 1. Roblox Window Detection & Focus

All scripts start by locating the Roblox window via process enumeration:

```python
# Find Roblox.exe process, then get its window handle via Win32
get_roblox_hwnd()  # Returns hwnd or None
get_roblox_region()  # Returns (left, top, width, height) tuple
focus_roblox()  # Maximizes and brings window to foreground
```

**Why**: Automation fails silently if Roblox isn't focused. Always call `focus_roblox()` before starting detection loops.

### 2. Vision Detection Loop Pattern

All bots follow this reactive pattern (see `dungeon_navigation.py` and `example_bot.py`):

1. Capture screen at Roblox region
2. Search for text via OCR or images via template matching
3. If found → execute action queue via ReactionHandler
4. Small delay, repeat

```python
vision = VisionModule(get_roblox_region())
handler = ReactionHandler()
while not stop_flag:
    screenshot = vision.capture_screen()
    text = vision.extract_text()
    if "play" in text.lower():
        handler.click(detected_x, detected_y)
        handler.execute_queue()
    time.sleep(0.5)
```

### 3. Human-Like Input Simulation

Critical pattern for avoiding detection:

- **Mouse movement**: Uses easing curves (cosine interpolation) over multiple small steps (~0.0012s intervals)
- **Action delays**: Random small delays between actions (0.05-0.2s)
- **Use `pydirectinput`**: More reliable than `pyautogui` for actual game input

See `acc_ranked.py:human_move()` for reference:

```python
def human_move(x, y, steps=3):
    # Eased movement with random small intervals
    ease = (1 - math.cos(t * math.pi)) / 2  # Smooth easing
    time.sleep(random.uniform(0.0012, 0.0015))
```

### 4. Action Queueing Pattern (ReactionHandler)

Instead of immediate execution, queue actions and execute atomically:

```python
handler = ReactionHandler()
handler.click(x, y, delay=0.1)  # Queues click
handler.drag(x1, y1, x2, y2)     # Queues drag
handler.key_press('space')        # Queues key
handler.execute_queue()           # Executes all in sequence
```

**Why**: Avoids partial execution if a detection changes mid-action.

### 5. Trigger Registration Pattern

ReactionHandler supports text and image triggers:

```python
handler.register_text_trigger("disconnect", on_disconnect_handler)
handler.register_image_trigger("button.png", on_button_found_handler)

# In main loop:
handler.process_text_triggers(detected_text)
handler.process_image_triggers(detected_images)
```

## Key Dependencies & Setup

| Package                   | Purpose                                | Special Notes                                                          |
| ------------------------- | -------------------------------------- | ---------------------------------------------------------------------- |
| `pyautogui`               | Screen capture, image detection        | Use `locateCenterOnScreen()` with confidence 0.7-0.9                   |
| `pytesseract` + Tesseract | OCR text extraction                    | Must install Tesseract separately at `C:\Program Files\Tesseract-OCR\` |
| `pydirectinput`           | Input simulation (mouse, keyboard)     | More reliable than `pyautogui.click()`; use for actual game input      |
| `psutil` + `win32*`       | Roblox process/window detection        | Required for robust window focusing                                    |
| `keyboard`                | Global hotkey (`Ctrl+Shift+P` to stop) | Every script must bind stop hotkey early                               |

## Common Gotchas & Conventions

### Image Template Matching

- **Confidence threshold**: Start with 0.8, lower to 0.7 if detection misses
- **Region optimization**: Always pass region to `locateCenterOnScreen()` to search only Roblox window, not full screen
- **PNG format**: Button screenshots must exactly match in-game UI; regenerate if game UI updates

### OCR Text Extraction

- **Case-insensitive**: Convert to `.lower()` before comparing (game text is inconsistent)
- **Whitespace**: Use `.strip()` and check substrings with `in` operator
- **Partial matches**: Game messages often include extra text; use "reconnect" not exact "Reconnect Please"

### Input Reliability

- Always `focus_roblox()` before simulation starts
- Use `pydirectinput` for clicks/drags, `pyautogui` only for detection
- Add `time.sleep()` between actions; game is slow to respond
- Test with small confidence/tolerance first, increase if flaky

### Process Detection

- Roblox may spawn as `RobloxPlayerBeta.exe` or similar; use `.lower()` substring match
- Window title often starts with game name, not always "Roblox"
- Always handle `get_roblox_hwnd() == None` gracefully

## Testing & Debugging

### Manual Testing Workflow

1. **Prepare image templates**: Take screenshots of buttons, save as PNG in script directory
2. **Run in test mode**: Add logging, print coordinates found
3. **Adjust confidence**: If `locateCenterOnScreen()` fails, lower confidence
4. **Adjust OCR region**: If text extraction is wrong, crop region tighter or adjust Tesseract lang

### Logging Best Practices

```python
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.info(f"Found button at {location}")  # For traces
```

All modules use `logging`; enable it for debugging. Avoid `print()` in library code.

### Common Debug Commands

```python
# Test image detection
vision.find_image("button.png", confidence=0.7)

# Test OCR
text = vision.extract_text()
print(f"OCR Result: '{text}'")

# Test window detection
print(get_roblox_region())
```

## File Organization

- **Root level**: Core modules (`vision_module.py`, `reaction_handler.py`) + example bots
- **`ranked/`**: Ranked mode specific automation
- **`afk_reconnect/`**: AFK handling (disconnect/reconnect monitoring)
- **All relative imports**: Assume scripts run from their own directory or root

## Refactored Architecture (New)

To improve code reusability and reduce duplication, refactored utilities are available:

### New Utility Modules

- **`windows_manager.py`**: Centralized Roblox window detection/focusing (eliminates duplication)
- **`input_simulator.py`**: Human-like input with configurable behavior parameters
- **`button_detector.py`**: Configuration-driven button detection (find, click, cache)
- **`config.py`**: Centralized configuration (Tesseract path, button templates, timeouts)

### Using Refactored Modules

```python
from config import TESSERACT_PATH, BUTTONS_DIR
from windows_manager import RobloxWindowManager
from input_simulator import InputSimulator
from button_detector import ButtonDetector, ButtonActions

# Setup
window_mgr = RobloxWindowManager()
input_sim = InputSimulator()
detector = ButtonDetector(BUTTONS_DIR)
actions = ButtonActions(detector, input_sim)

# Use
window_mgr.focus_roblox()
region = window_mgr.get_roblox_region()
input_sim.wiggle_and_click(x, y)
actions.click_button("fight", region=region)
```

## Installation & Setup

Run `python setup.py` to automatically:

- Install all Python dependencies
- Download and install Tesseract OCR
- Create project directory structure
- Validate installation
- Generate button template guide

**Refactored bot examples**:

- `ranked/acc_ranked_refactored.py` - Updated ranked mode bot using new utilities
- `afk_reconnect/afk_monitor_refactored.py` - Updated AFK monitor

## Future Extension Points

1. **Add new reaction type**: Extend `ActionType` enum and `ReactionHandler.execute_action()`
2. **Multi-region detection**: Extend `VisionModule` to handle multiple game regions simultaneously
3. **Event-driven architecture**: Replace polling loops with callback-based triggers
4. **Config file support**: Load button templates from JSON config instead of hardcoding
