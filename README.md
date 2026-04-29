# Auto Brightness Adjuster - Installation Guide

## What This Does
Uses your Lenovo X1 Carbon's webcam to detect ambient light and automatically adjusts your screen brightness.

## Requirements
- Python 3.7 or higher
- Windows (tested on Windows 10/11)
- Administrator privileges (for brightness control)

## Installation Steps

### 1. Clone the Repo
Open Command Prompt and run:
```cmd
cd C:\Users\James\Documents\Scripts
git clone https://github.com/Bajeejames7/auto-brightness-program-windows.git
cd auto-brightness-program-windows
```

### 2. Install Python
If you don't have Python installed:
- Download from https://www.python.org/downloads/
- During installation, CHECK "Add Python to PATH"

### 3. Install Dependencies
```cmd
pip install -r requirements.txt
```

## Usage

### Standard Mode
1. Open Command Prompt **as Administrator** (right-click → "Run as administrator")
2. Navigate to the script folder:
```cmd
cd C:\Users\James\Documents\Scripts\auto-brightness-program-windows
```
3. Run:
```cmd
python auto_brightness.py
```

### Stealth Mode
Stealth mode is the default behavior of this script. It's designed to minimize how long the camera LED stays on and reduce CPU usage.

How it works:
- Opens the webcam for a single frame capture using `CAP_DSHOW` (bypasses Windows Media Foundation overhead)
- Requests the smallest possible frame buffer (16x16) to speed up capture
- Releases the camera immediately after — the LED turns off right away
- Only adjusts brightness if the change is greater than 10% (avoids unnecessary CPU wake-ups)
- Polls every 60 seconds by default to preserve battery life

To run in stealth mode (it's just the normal run command):
```cmd
cd C:\Users\James\Documents\Scripts\auto-brightness-program-windows
python auto_brightness.py
```

You'll see output like:
```
=== Stealth Auto-Brightness Active ===
Polling every 60s. Run as Admin for best results.
Adjusted: 72% (Light: 48%)
```

The camera light will flicker briefly every 60 seconds, then go dark — that's expected.

#### Tuning Stealth Behavior
Edit these values in `auto_brightness.py`:

| Variable | Default | Effect |
|---|---|---|
| `INTERVAL` | `60` | Seconds between checks. Higher = less battery use |
| `camera_index` | `0` | Change to `1` if wrong camera is used |
| `abs(target - last_b) > 10` | `10` | Minimum % change to trigger an adjustment |

## Troubleshooting

### "Could not open webcam"
- Make sure no other program is using the camera
- Try changing `camera_index=0` to `camera_index=1` in the script

### Brightness not changing
- Make sure you're running as Administrator
- Some laptops require special drivers — the script will notify you

### Camera light stays on longer than expected
- This is normal on first run while the camera initializes
- If it stays on continuously, check that `cap.release()` wasn't accidentally removed

### Adjustments too aggressive/slow
- Increase `INTERVAL` for less frequent checks
- Lower the `> 10` threshold if you want more sensitive adjustments

## Running on Startup (Optional)

### Windows Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: "At log on"
4. Action: "Start a program"
5. Program: `C:\Path\To\Python\python.exe`
6. Arguments: `C:\Users\James\Documents\Scripts\auto-brightness-program-windows\auto_brightness.py`
7. Check "Run with highest privileges"

### Or Create a Shortcut
1. Right-click desktop → New → Shortcut
2. Location: `python C:\Users\James\Documents\Scripts\auto-brightness-program-windows\auto_brightness.py`
3. Right-click shortcut → Properties → Advanced
4. Check "Run as administrator"
