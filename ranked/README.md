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
The script uses image matching for buttons. You need to create or obtain the following PNG files and place them in the same directory as the script:

- `fight_button.png` - Screenshot of the "Fight" button
- `ranked_button.png` - Screenshot of the "Ranked" button  
- `refresh_button.png` - Screenshot of the "Refresh" button

Take screenshots of these buttons from your Roblox game and save them as PNG files with the exact names above.

## 4. Run the Script
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