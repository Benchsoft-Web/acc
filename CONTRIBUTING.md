# Contributing Guide

Thank you for contributing! This guide covers architecture, patterns, code standards, and how to extend the codebase.

## Architecture Overview

### Core Components

**Vision Module** (`vision_module.py`)

- Screen capture via `pyautogui`
- Image detection with configurable confidence
- OCR text extraction via Tesseract

**Reaction Handler** (`reaction_handler.py`)

- Action queueing system
- Atomic execution (all-or-nothing)
- Text/image trigger registration

**Utilities (New in v2.0)**

- `config.py` - Centralized configuration
- `windows_manager.py` - Window operations
- `input_simulator.py` - Human-like input
- `button_detector.py` - Button detection with caching

### Critical Patterns

**1. Always Focus Roblox Before Detection**

```python
from windows_manager import RobloxWindowManager
mgr = RobloxWindowManager()
mgr.focus_roblox()  # Maximizes and brings to foreground
region = mgr.get_roblox_region()  # Get safe region for screenshot
```

**Why**: Automation fails silently if window isn't focused. This is the #1 gotcha.

**2. Use InputSimulator for All Input**

```python
from input_simulator import InputSimulator
input_sim = InputSimulator()
input_sim.human_move(x, y)  # Smooth easing
input_sim.wiggle_and_click(x, y)  # Anti-bot behavior
input_sim.press_key('space')  # Key presses
```

**Why**: Consistency across all bots, configurable behavior, human-like timing.

**3. Queue Actions Atomically**

```python
handler = ReactionHandler()
handler.click(x, y)
handler.drag(x1, y1, x2, y2)
handler.key_press('space')
handler.execute_queue()  # All-or-nothing execution
```

**Why**: Prevents partial execution if detection changes mid-action.

**4. Centralize Configuration**

```python
from config import TESSERACT_PATH, BUTTONS_DIR, IMAGE_CONFIDENCE
# Never hardcode paths or parameters
```

**Why**: Single source of truth, easy to adjust for different setups.

**5. Use ButtonDetector for Clicks**

```python
from button_detector import ButtonActions
actions = ButtonActions(detector, input_sim)
actions.click_button("fight", region=region)
actions.click_button("ranked", region=region, offset=(0, -15))
```

**Why**: One-liner clicks, automatic caching, consistent behavior.

## Code Standards

### Type Hints (Required)

```python
from typing import Optional, Tuple, List

def find_button(self, name: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
    """Find button center coordinates.

    Args:
        name: Button template name
        confidence: Match threshold (0.0-1.0)

    Returns:
        (x, y) coordinates or None if not found
    """
    pass
```

**Rule**: All function signatures must include type hints.

### Logging (Not Print)

```python
import logging

logger = logging.getLogger(__name__)

# User-facing
logger.info("Starting bot...")
logger.warning("Button not found, retrying")

# Developer debugging
logger.debug(f"Detected button at ({x}, {y})")

# Errors with traceback
logger.error("Failed to click button", exc_info=True)
```

**Rule**: Use logging instead of `print()` for library code.

### Docstrings (All Public Methods)

```python
def human_move(self, x: int, y: int, steps: int = 3) -> None:
    """Move mouse with smooth easing curve.

    Simulates human-like movement using cosine interpolation
    to avoid detection by anti-bot systems.

    Args:
        x: Target X coordinate
        y: Target Y coordinate
        steps: Number of intermediate steps (higher = smoother)

    Raises:
        ValueError: If coordinates out of screen bounds

    Example:
        >>> sim = InputSimulator()
        >>> sim.human_move(640, 480)  # Move to center of 1280x720 screen
    """
    pass
```

**Rule**: Public methods must have docstrings with Args, Returns, Raises.

### Error Handling

```python
def click_button(self, name: str) -> bool:
    try:
        location = self.detector.find_button(name)
        if location is None:
            logger.warning(f"Button '{name}' not found")
            return False
        self.input_sim.click(location[0], location[1])
        return True
    except FileNotFoundError:
        logger.error(f"Button template '{name}' not found in {BUTTONS_DIR}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error clicking button: {e}", exc_info=True)
        return False
```

**Rules**:

- Catch specific exceptions first
- Log all errors with context
- Return boolean or safe defaults
- Use `exc_info=True` for unexpected errors

### Naming Conventions

```python
# Classes: PascalCase
class RobloxWindowManager:
    pass

# Functions/methods: snake_case
def human_move(x, y):
    pass

# Constants: UPPER_SNAKE_CASE
DEFAULT_CONFIDENCE = 0.8
BUTTON_TEMPLATES = {...}

# Private: leading underscore
def _internal_helper():
    pass

# Booleans: is_/has_ prefix
is_running = True
has_buttons = False
```

**Rule**: Follow naming convention consistently.

## Adding New Features

### Step 1: Use Existing Utilities

Before writing code, check if a utility handles it:

| Need            | Use                                   |
| --------------- | ------------------------------------- |
| Window focusing | `windows_manager.RobloxWindowManager` |
| Mouse movement  | `input_simulator.InputSimulator`      |
| Button clicks   | `button_detector.ButtonActions`       |
| Configuration   | `config.py`                           |
| Screen capture  | `vision_module.VisionModule`          |
| Action queueing | `reaction_handler.ReactionHandler`    |

### Step 2: Extend Utilities if Needed

Add to existing class if it makes sense:

```python
# In input_simulator.py
def press_key(self, key: str, duration: float = 0.1) -> None:
    """Press and hold key."""
    pydirectinput.keyDown(key)
    time.sleep(duration)
    pydirectinput.keyUp(key)
```

Add to `config.py` if new configuration needed:

```python
# In config.py
DRAG_DURATION = 0.5  # Time for drag operations
DRAG_SMOOTHNESS = 20  # Intermediate steps
```

### Step 3: Document & Test

```python
def new_feature(param: str) -> bool:
    """New feature description.

    More detailed explanation of what it does
    and why it's useful.

    Args:
        param: What the parameter does

    Returns:
        True if successful, False otherwise

    Example:
        >>> new_feature("test")
        True
    """
    logger.info("Starting new feature")
    try:
        # Implementation
        logger.debug("Feature step 1 complete")
        return True
    except Exception as e:
        logger.error(f"Feature failed: {e}", exc_info=True)
        return False
```

## Creating New Bots

### Template

```python
#!/usr/bin/env python3
"""Bot for [game mode/task].

Automates [specific task] by detecting [visual elements]
and executing [actions].
"""

import logging
import time
import keyboard
from windows_manager import RobloxWindowManager
from input_simulator import InputSimulator
from button_detector import ButtonDetector, ButtonActions
from config import BUTTONS_DIR

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MyBot:
    def __init__(self):
        self.window_mgr = RobloxWindowManager()
        self.input_sim = InputSimulator()
        self.detector = ButtonDetector(BUTTONS_DIR)
        self.actions = ButtonActions(self.detector, self.input_sim)
        self.stop_flag = False

    def setup(self) -> bool:
        """Prepare environment."""
        logger.info("Setting up bot...")
        self.window_mgr.focus_roblox()
        time.sleep(1)
        return True

    def action_sequence(self) -> bool:
        """Execute main action."""
        self.actions.click_button("fight")
        time.sleep(0.5)
        return True

    def run(self) -> None:
        """Main loop."""
        def stop_bot():
            self.stop_flag = True
            logger.info("Stop signal received")

        keyboard.add_hotkey('ctrl+shift+p', stop_bot)

        if not self.setup():
            logger.error("Setup failed")
            return

        logger.info("Bot running (Ctrl+Shift+P to stop)")
        while not self.stop_flag:
            try:
                self.action_sequence()
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error in action: {e}", exc_info=True)
                time.sleep(1)

        logger.info("Bot stopped")

if __name__ == '__main__':
    bot = MyBot()
    bot.run()
```

## Debugging Tips

### Enable Debug Logging

```python
logging.basicConfig(level=logging.DEBUG)  # Instead of INFO
```

This shows:

- Detected button coordinates
- Vision module results
- Input simulation details
- All function entry/exit points

### Test Image Detection

```python
from vision_module import VisionModule
from windows_manager import RobloxWindowManager

mgr = RobloxWindowManager()
region = mgr.get_roblox_region()
vision = VisionModule(region)

# Test find
location = vision.find_image("buttons/fight_button.png", confidence=0.7)
print(f"Found fight button at: {location}")

# Test OCR
text = vision.extract_text()
print(f"OCR result: {text}")
```

### Test Button Detector

```python
from button_detector import ButtonDetector
from config import BUTTONS_DIR

detector = ButtonDetector(BUTTONS_DIR)
location = detector.find_button("fight", confidence=0.7)
print(f"Fight button: {location}")
```

## Button Detection Patterns

### Button Naming Convention

All button templates should follow this naming scheme:

- Use **simple names** without suffix: `fight.png`, not `fight_button.png`
- Names are **case-sensitive** and must match `config.py`'s `BUTTON_TEMPLATES` dict
- Standardized buttons: `fight`, `ranked`, `refresh`, `reconnect`, `enter_dungeon`, `leave_dungeon`

### Adding New Buttons

1. **Take screenshot** of button in Roblox (use `Win+Shift+S`)
2. **Crop tightly** - just the button, no extra UI
3. **Save as PNG** in `buttons/` directory with simple name (e.g., `mybtn.png`)
4. **Add to config.py**:
   ```python
   BUTTON_TEMPLATES = {
       "mybtn": "mybtn.png",
       # ... other buttons
   }
   ```
5. **Use in code**:
   ```python
   actions.click_button("mybtn")  # One-liner
   ```

### Button Detection Tips

- **Full screen search**: Detection searches entire screen (no region constraint for reliability)
- **Confidence tuning**: Start with 0.8, lower to 0.7 if detection misses
- **Size matters**: Smaller templates (50-100px) are faster and more reliable than large ones
- **Contrast important**: Buttons should have clear edges; poor lighting/contrast reduces detection
- **Regenerate if UI changes**: Game UI updates require new screenshots

### Common Issues

**"Button not found" warning**

- Verify template exists: `buttons/mybtn.png`
- Check exact name matches `config.py`
- Retake screenshot if game UI changed
- Lower confidence threshold (0.7-0.8)

**Low detection reliability**

- Ensure button has clean edges and high contrast
- Crop template tightly (avoid surrounding UI)
- Use smaller templates when possible
- Test with debug logging enabled

### Common Issues

**Image not found**

- Lower confidence: 0.8 → 0.7
- Verify file exists: `buttons/fight_button.png`
- Retake screenshot if game UI changed
- Check file format: Must be PNG

**OCR returns garbage**

- Crop region tighter in vision module
- Ensure text is clear and high contrast
- Increase region size if text is small
- Check Tesseract installed correctly

**Script clicks wrong location**

- Verify button template position
- Check offset values in config
- Print detected coordinates before clicking
- Regenerate template if game UI changed

## Performance Optimization

### Caching

```python
# ButtonDetector already caches button locations
# For repeated clicks on same button, it reuses location
detector.clear_cache()  # Reset if UI changes
```

### Reduce OCR Calls

```python
# ❌ Bad: OCR every loop iteration
while True:
    text = vision.extract_text()
    if "play" in text:
        click_button()

# ✅ Good: OCR every N iterations
counter = 0
while True:
    if counter % 5 == 0:  # Every 5 loops
        text = vision.extract_text()
    if "play" in text:
        click_button()
    counter += 1
```

### Region Optimization

```python
# ❌ Bad: Search full Roblox region
image = pyautogui.locateCenterOnScreen("button.png")

# ✅ Good: Search specific region
button_region = (x, y, width, height)
image = pyautogui.locateCenterOnScreen(
    "button.png",
    region=button_region,
    confidence=0.8
)
```

## Testing

### Manual Testing Checklist

- [ ] Window detection finds Roblox
- [ ] Focus command maximizes window
- [ ] Button detection works (correct coordinates)
- [ ] Click actions execute (visible feedback)
- [ ] Input simulation smooth (not jerky)
- [ ] OCR extracts text correctly
- [ ] Stop hotkey (Ctrl+Shift+P) works
- [ ] Error recovery graceful

### Automated Testing (Future)

```python
import unittest
from button_detector import ButtonDetector

class TestButtonDetector(unittest.TestCase):
    def test_find_button_valid(self):
        detector = ButtonDetector(BUTTONS_DIR)
        location = detector.find_button("fight")
        self.assertIsNotNone(location)
```

## Submitting Changes

1. **Create feature branch**: `git checkout -b feature/my-feature`
2. **Follow code standards**: Type hints, logging, docstrings
3. **Test thoroughly**: Manual testing + debug output
4. **Add to RELEASES.md**: Document your changes
5. **Keep backward compatible**: Don't break original scripts
6. **Submit pull request**: With description of changes

## Useful References

- **Architecture**: See `.github/copilot-instructions.md` for detailed patterns
- **Configuration**: See `config.py` for all settings
- **Utilities**: See `windows_manager.py`, `input_simulator.py`, `button_detector.py` for available methods
- **Examples**: See `ranked/acc_ranked_refactored.py`, `afk_reconnect/afk_monitor_refactored.py`

## Common Questions

**Q: Can I use this on macOS/Linux?**
A: No, requires Windows win32 APIs. Would need major refactor for cross-platform.

**Q: How do I speed up automation?**
A: See Performance Optimization section. Reduce delays in config, limit OCR calls, use button caching.

**Q: Can I automate multiple accounts?**
A: Yes, create separate instances of bot class with separate configurations.

**Q: What about anti-bot detection?**
A: Human-like input (easing, random delays) helps. But if Roblox implements anti-automation, unlikely to bypass. Use responsibly.

**Q: How to debug window detection?**
A: Add `logger.setLevel(logging.DEBUG)` and check output for window handles found.

---

**Last Updated**: December 2025 | **Version**: 2.0
