#!/usr/bin/env python3
"""
Roblox Automation Setup Script
Installs all dependencies, Tesseract, and validates the installation
Run as: python setup.py
"""

import sys
import os
import subprocess
import platform
import urllib.request
import zipfile
import shutil
from pathlib import Path
import json

# Enable UTF-8 output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    print(f"[OK] {text}")

def print_error(text):
    print(f"[ERROR] {text}")

def print_warning(text):
    print(f"[WARN] {text}")

def print_info(text):
    print(f"[INFO] {text}")

def check_os():
    """Verify we're running on Windows"""
    if platform.system() != "Windows":
        print_error("This setup script only works on Windows")
        print_info("You're running: " + platform.system())
        sys.exit(1)
    print_success("Windows detected")

def check_python():
    """Verify Python 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python 3.8+ required, but you have {version.major}.{version.minor}")
        sys.exit(1)
    print_success(f"Python {version.major}.{version.minor} detected")

def install_pip_packages():
    """Install required Python packages"""
    print_header("Installing Python Packages")
    
    packages = [
        "pyautogui",
        "pydirectinput",
        "pytesseract",
        "pillow",
        "psutil",
        "pywin32",
        "keyboard",
    ]
    
    print_info("Installing packages (this may take a minute)...")
    try:
        for package in packages:
            print(f"  Installing {package}...", end=" ", flush=True)
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-q", package],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"\n[ERROR] Failed to install {package}")
                print(result.stderr)
                return False
            print("done")
        print_success("All Python packages installed")
        return True
    except Exception as e:
        print_error(f"Failed to install packages: {e}")
        return False

def download_tesseract():
    """Download Tesseract installer from GitHub"""
    print_header("Setting Up Tesseract OCR")
    
    tesseract_path = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    
    if tesseract_path.exists():
        print_success("Tesseract already installed at " + str(tesseract_path))
        return True
    
    print_info("Downloading Tesseract installer...")
    print_info("(This is a ~100MB download)")
    
    installer_url = "https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.0/tesseract-ocr-w64-setup-v5.3.0.exe"
    installer_path = Path(os.getenv('TEMP')) / "tesseract-installer.exe"
    
    try:
        urllib.request.urlretrieve(installer_url, installer_path)
        print_success("Downloaded Tesseract installer")
        
        print_info("Running Tesseract installer...")
        print_warning("Please complete the installation wizard (use default settings)")
        input("Press Enter when ready to continue...")
        
        os.startfile(installer_path)
        
        # Wait for installation
        print_info("Waiting for installation to complete (max 5 minutes)...")
        import time
        for i in range(300):
            if tesseract_path.exists():
                print_success("Tesseract installed successfully!")
                installer_path.unlink()
                return True
            time.sleep(1)
            if i % 30 == 0:
                print("  Still waiting...", end="\r")
        
        print_error("Tesseract installation timeout or failed")
        return False
        
    except Exception as e:
        print_error(f"Failed to download/install Tesseract: {e}")
        print_info("You can install it manually from:")
        print_info("  https://github.com/UB-Mannheim/tesseract/wiki/Downloads")
        print_warning("Make sure to install it to: C:\\Program Files\\Tesseract-OCR\\")
        return False

def create_project_structure():
    """Create necessary directories"""
    print_header("Setting Up Project Structure")
    
    project_root = Path(__file__).parent
    dirs_to_create = [
        project_root / "buttons",
        project_root / "ranked" / "buttons",
        project_root / "afk_reconnect" / "buttons",
        project_root / ".github",
    ]
    
    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
        print_info(f"Created/verified: {dir_path.relative_to(project_root)}")
    
    print_success("Project structure ready")

def create_example_buttons_readme():
    """Create a README for button template directory"""
    print_header("Creating Button Template Guide")
    
    project_root = Path(__file__).parent
    buttons_dir = project_root / "buttons"
    readme_path = buttons_dir / "README_BUTTONS.md"
    
    readme_content = """# Button Templates

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
"""
    
    readme_path.write_text(readme_content)
    print_success(f"Created: {readme_path.relative_to(project_root)}")

def validate_installation():
    """Verify all dependencies are installed"""
    print_header("Validating Installation")
    
    errors = []
    
    # Check Python packages
    packages_to_check = [
        "pyautogui",
        "pydirectinput",
        "pytesseract",
        "PIL",
        "psutil",
        "win32gui",
        "keyboard",
    ]
    
    for package in packages_to_check:
        try:
            __import__(package)
            print_success(f"{package}")
        except ImportError:
            print_error(f"{package}")
            errors.append(package)
    
    # Check Tesseract
    tesseract_path = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    if tesseract_path.exists():
        print_success(f"Tesseract OCR")
    else:
        print_error(f"Tesseract OCR (not found at {tesseract_path})")
        errors.append("Tesseract")
    
    # Check project structure
    required_files = [
        "config.py",
        "windows_manager.py",
        "input_simulator.py",
        "button_detector.py",
        "buttons/README_BUTTONS.md",
    ]
    
    project_root = Path(__file__).parent
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print_success(f"{file_path}")
        else:
            print_error(f"{file_path}")
            errors.append(file_path)
    
    if errors:
        print_error(f"\nFound {len(errors)} issues:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print_success("All validations passed!")
        return True

def print_final_instructions():
    """Print next steps"""
    print_header("Setup Complete!")
    
    print_info("Next Steps:")
    print("  1. Create button templates:")
    print("     - Take PNG screenshots of game buttons")
    print("     - Save to: ./buttons/")
    print("     - See buttons/README_BUTTONS.md for details")
    print()
    print("  2. Run a bot:")
    print("     - Ranked mode: python ranked/acc_ranked.py")
    print("     - AFK monitor: python afk_reconnect/afk_monitor.py")
    print()
    print("  3. Stop the bot anytime with: Ctrl+Shift+P")
    print()
    print_success("Happy automating!")

def main():
    """Run setup"""
    print_header("Roblox Automation Scripts - Setup Wizard")
    
    # Run all setup steps
    check_os()
    check_python()
    
    if not install_pip_packages():
        print_error("\nSetup failed. Please fix the errors above and try again.")
        sys.exit(1)
    
    if not download_tesseract():
        print_warning("Tesseract installation failed. You can install it manually later.")
        print_warning("(The bot will not work without it)")
    
    create_project_structure()
    create_example_buttons_readme()
    
    if validate_installation():
        print_final_instructions()
    else:
        print_error("Some issues were found. Please fix them and try again.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\n\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
