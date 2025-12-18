# Setup Instructions for acc_ranked.py

This Python script automates interactions in Roblox using image recognition and OCR. Follow these steps to set it up and run.

## Prerequisites

- Windows operating system (required for win32 libraries)
- Python 3.8+ installed
- Roblox game client running

## 1. Install Required Python Packages

Run the following command in your terminal (preferably in a virtual environment):

```
pip install pyautogui pydirectinput pytesseract pillow psutil pywin32 keyboard
```

## 2. Install Tesseract OCR

The script uses Tesseract for optical character recognition (OCR) to detect text like "reconnect" and "dismiss".

1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install it to the default location: `C:\Program Files\Tesseract-OCR\`
3. The script is already configured to look for `tesseract.exe` at that path. If you installed it elsewhere, update the path in the script:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"YOUR_PATH_TO\tesseract.exe"
   ```

## 3. Prepare Image Templates

The script uses image matching for buttons. The following PNG files should be included with the script in the same directory. If they're not present, you'll need to create them by taking screenshots of the buttons in your Roblox game:

- `fight_button.png` - Screenshot of the "Fight" button
- `ranked_button.png` - Screenshot of the "Ranked" button  
- `refresh_button.png` - Screenshot of the "Refresh" button

### How to Create the Image Templates:

1. Launch Roblox and navigate to the game screen where these buttons appear.
2. Use Windows Snipping Tool, Snip & Sketch, or any screenshot tool to capture each button.
3. Crop the image to include only the button (avoid extra UI elements).
4. Save each as a PNG file with the exact names listed above.
5. Place the PNG files in the same directory as `acc_ranked.py`.

**Note:** The images need to match the in-game buttons exactly for reliable detection. If the game's UI changes, you may need to update these templates.

1. Ensure Roblox is running and the game window is visible.
2. Open a terminal and navigate to the directory containing `acc_ranked.py`:
   ```
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
