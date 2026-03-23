"""
MORIS UNIVERSAL LICENSE (MUL) - Version 1.0
Copyright (c) moris

This software is licensed under the MORIS UNIVERSAL LICENSE (MUL).
By downloading, copying, or running this software, you agree to accept all terms and conditions
of the MUL license, which are included in the accompanying LICENSE.md file.

KEY TERMS:
- Personal use only (non-commercial)
- Attribution to original author is REQUIRED
- Commercial use is strictly prohibited
- Redistribution without license and attribution is prohibited
- Personal modifications allowed, but derivatives must retain original credit
- NO WARRANTY - use at your own risk

Full license text: See LICENSE.md
For support: https://discord.gg/2fraBuhe3m
"""

import json
import sys
from copy import deepcopy
from typing import Any, Optional

from .constants import DEFAULT_SETTINGS, REG_PATH

if sys.platform == "win32":
    import winreg


def _reg_write(key_path: str, name: str, value: Any) -> None:
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
        if isinstance(value, bool):
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, int(value))
        elif isinstance(value, int):
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
        elif isinstance(value, (float, str)):
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, str(value))


def _reg_read(key_path: str, name: str, default: Any) -> Any:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            raw, _ = winreg.QueryValueEx(key, name)
            if isinstance(default, bool):
                return bool(int(raw))
            if isinstance(default, int):
                return int(raw)
            if isinstance(default, float):
                return float(raw)
            return raw
    except (FileNotFoundError, OSError, ValueError):
        return default


def save_settings(settings: dict, profiles: dict) -> None:
    if sys.platform != "win32":
        return
    for key, value in settings.items():
        if isinstance(value, (str, int, float, bool)):
            _reg_write(REG_PATH, key, value)
    _reg_write(REG_PATH, "_profiles", json.dumps(profiles))


def load_settings() -> tuple[dict, dict]:
    if sys.platform != "win32":
        return deepcopy(DEFAULT_SETTINGS), {}

    settings: dict = deepcopy(DEFAULT_SETTINGS)
    for key, default in DEFAULT_SETTINGS.items():
        if isinstance(default, (str, int, float, bool)):
            settings[key] = _reg_read(REG_PATH, key, default)

    raw_profiles = _reg_read(REG_PATH, "_profiles", "{}")
    try:
        profiles: dict = json.loads(raw_profiles)
    except (json.JSONDecodeError, TypeError):
        profiles = {}

    return settings, profiles


def export_profile(settings: dict, path: str) -> None:
    skip = {"visible"}
    export_data = {k: v for k, v in settings.items() if k not in skip}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(export_data, fh, indent=2)


def import_profile(path: str) -> Optional[dict]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        result = deepcopy(DEFAULT_SETTINGS)
        result.update({k: v for k, v in data.items() if k in DEFAULT_SETTINGS})
        return result
    except (OSError, json.JSONDecodeError, TypeError):
        return None
