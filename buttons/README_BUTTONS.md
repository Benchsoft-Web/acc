# Button Templates

This directory should contain PNG screenshots of game buttons for automated detection.

## Button Naming Convention

Button templates should use simple names without suffix:
- `fight.png` (not `fight_button.png`)
- `ranked.png` (not `ranked_button.png`)
- `refresh.png` (not `refresh_button.png`)
- `reconnect.png`
- `enter_dungeon.png`
- `leave_dungeon.png`

## How to Create Templates

1. Launch Roblox and navigate to where the button appears
2. Use Windows Snipping Tool (Win+Shift+S) to capture just the button
3. Crop to include only the button (avoid extra UI)
4. Save as PNG with the simple name from the list above
5. Place in this directory

## Tips for Good Detection

- Take screenshots at the same resolution you'll run the bot at
- Ensure clean lighting and contrast
- Buttons must be fully visible and unobstructed
- If detection fails, try lowering confidence threshold in config.py (0.7-0.8)
- If UI changes, regenerate the templates

## Testing Detection

```python
from button_detector import ButtonDetector
from pathlib import Path

detector = ButtonDetector(Path(__file__).parent)
result = detector.find_button("fight")
print(f"Fight button found at: {result}")
```
