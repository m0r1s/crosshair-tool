# crosshair tool

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) [![License: MUL](https://img.shields.io/badge/license-MUL-orange.svg)](LICENSE.md) [![Platform: Windows](https://img.shields.io/badge/platform-Windows-informational.svg)](https://www.microsoft.com/windows) [![Discord](https://img.shields.io/badge/Discord-Join-5865F2.svg)](https://discord.com/invite/2fraBuhe3m)

A lightweight crosshair overlay tool for Windows. Customise your crosshair once, then have it on screen instantly with full control over shape, color, zoom, and hotkeys.

---

## Features

- **Crosshair Customisation** - Adjust length, thickness, gap, and opacity; toggle each arm independently
- **Color Picker** - Full color wheel, hex input, and preset swatches; separate color for outline
- **Outline & Center Dot** - Optional outline with configurable thickness and color; optional center dot with configurable size
- **Zoom Overlay** - Real-time magnified view of the screen center for long range fights; configurable zoom factor and window size
- **Zoom Modes** - Hold-to-zoom or click-to-toggle; position the zoom window below, above, left, right, middle, or at a custom coordinate
- **Custom Hotkeys** - Bind any keyboard key or mouse button (MB1-MB5) to toggle visibility or trigger zoom
- **Right-Click Hide** - Automatically hide the crosshair while right mouse button is held or toggled
- **Profile Management** - Save, load, and delete named crosshair profiles; export and import as JSON files
- **Auto-Save** - Every setting change is saved automatically and restored on next launch
- **Always-on-Top Pin** - Pin the settings window above other windows when needed
- **Reset Settings** - Restore all settings to defaults in one click
- **Discord** - Quick link to the community Discord from within the app

---

## System Requirements

- **OS**: Windows 10 or later
- **Python**: 3.10 or higher
- **Dependencies**: PySide6, pynput

---

## Installation

### Option 1: From Source

```bash
git clone https://github.com/m0r1s/crosshair.git
cd crosshair
pip install PySide6 pynput
cd src
python -m crosshair
```

### Option 2: Windows Standalone (.exe)

Download the latest release from the [Releases](https://github.com/m0r1s/crosshair/releases) page and run the `.exe` - no Python required.

### Troubleshooting Installation

**`python` is not recognized**
- Reinstall Python and check "Add Python to PATH" during setup

**`No module named 'PySide6'`**
- Run: `pip install PySide6 pynput`

**`pynput` fails to install**
- Install [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/), then retry

---

## Quick Start

### 1. Launch
- Run `python -m crosshair`
- The settings window opens with a live crosshair preview

### 2. Customise Your Crosshair
- Adjust length, thickness, gap, color, and opacity in the Crosshair and Color cards
- Toggle individual arms by clicking them in the preview

### 3. Set Up Hotkeys
- Bind a key or mouse button to toggle visibility
- Enable zoom and bind a trigger key in the Zoom card

### 4. Save a Profile
- Name your setup and hit Save in the Profiles card to keep multiple configurations

---

## Performance & Limitations

### What Works Well

- FPS and third-person shooter games without anti-cheat overlays
- Any game or application where a static screen overlay is useful
- Long range PvP with the zoom overlay

### Known Limitations

- **Anti-cheat** - games with kernel-level anti-cheat may detect or block overlays
- **Windows only** - macOS and Linux are not currently supported

---

## Roadmap

### Completed
- Crosshair shape, color, outline, and center dot customisation
- Per-arm visibility toggle
- Zoom overlay with hold/toggle modes and position anchors
- Keyboard and mouse button hotkey binding
- Right-click hide (hold and toggle modes)
- Named profile save/load with JSON export/import
- Auto-save
- Reset settings to defaults
- Discord quick link

### Planned
- [ ] Animated crosshair (spread on movement or fire)
- [ ] Multiple crosshair presets with quick-switch hotkey
- [ ] Custom crosshair images

---

## Architecture

```
crosshair/
├── main.py                      Entry point
├── overlay.py                   Crosshair overlay window
├── zoom_overlay.py              Zoom overlay window
├── hotkeys.py                   Global keyboard and mouse listener
├── ui/
│   ├── main_window.py           Settings window
│   ├── widgets.py               UI components
│   └── styles.py                Qt stylesheets
└── utils/
    ├── constants.py             App-wide constants and assets
    └── settings.py              Save/load logic
```

---

## License

This project is licensed under the **MORIS UNIVERSAL LICENSE (MUL)** - see [LICENSE.md](LICENSE.md) for full terms.

**Summary:**
- Personal, non-commercial use only
- Attribution to the original author is required
- Commercial use and redistribution without the license are prohibited

---

## Support

- **Discord**: [discord.com/invite/2fraBuhe3m](https://discord.com/invite/2fraBuhe3m)
- **Issues**: Open a GitHub issue with your Windows version, Python version, and steps to reproduce

When reporting a bug, include:
1. Windows version
2. Python version (`python --version`)
3. Steps to reproduce
4. Error message or screenshot

---

## Show Your Support

If crosshair tool improves your aim, consider starring the repo on GitHub - it helps others find the project.

Made with ♡ by _**moris**_ and _**tim**_
