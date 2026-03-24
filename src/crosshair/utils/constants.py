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

import sys
from dataclasses import dataclass

APP_NAME    = "moris crosshair tool"
APP_VERSION = "2.1.1"

REG_PATH          = r"Software\moris\crosshair_tool"
REG_PROFILES_PATH = r"Software\moris\crosshair_tool\profiles"

COLOR_PRESETS: dict[str, str] = {
    "Green":   "#00FF00",
    "Red":     "#FF4040",
    "Blue":    "#4499FF",
    "White":   "#FFFFFF",
    "Yellow":  "#FFFF00",
    "Cyan":    "#00FFFF",
    "Magenta": "#FF44FF",
    "Orange":  "#FFA500",
    "Pink":    "#FF69B4",
    "Teal":    "#00D4AA",
}

DEFAULT_SETTINGS: dict = {
    "length":            8,
    "thickness":         2,
    "gap":               4,
    "color":             "#00FF00",
    "opacity":           220,
    "outline_enabled":   False,
    "outline_color":     "#000000",
    "outline_thickness": 1,
    "dot_enabled":       False,
    "dot_size":          3,
    "line_top":          True,
    "line_bottom":       True,
    "line_left":         True,
    "line_right":        True,
    "visible":           True,
    "right_click_hide":  True,
    "right_click_mode":  "hold",
    "toggle_hotkey":     "",
    "zoom_enabled":      True,
    "zoom_hotkey":       "c",
    "zoom_mode":         "hold",
    "zoom_size":         300,
    "zoom_factor":       2.0,
    "zoom_anchor":       "middle",
    "zoom_x":            0,
    "zoom_y":            0,
    "resolution":        "16:9",
}

@dataclass(frozen=True)
class _C:
    bg_main:    str = "#121212"
    bg_dark:    str = "#0a0a0a"
    fg:         str = "#f0f0f0"
    fg_muted:   str = "#7a7a7a"
    accent:     str = "#89dfff"
    accent_red: str = "#ff4b69"

C = _C()

FONT = "'Segoe UI', Arial" if sys.platform == "win32" else "Arial"

SW_W:    int   = 40
SW_H:    int   = 20
TRACK_H: int   = 14
TRACK_Y: float = (SW_H - TRACK_H) / 2
KNOB_D:  int   = 18
KNOB_Y:  float = (SW_H - KNOB_D) / 2
KNOB_OFF: int  = 1
KNOB_TRAV: int = SW_W - KNOB_D - KNOB_OFF - 2

TRACK_ON:  tuple = (0x89, 0xDF, 0xFF)
TRACK_OFF: tuple = (0x28, 0x28, 0x28)

SVG_PIN: bytes = (
    b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
    b'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    b'stroke-linejoin="round"><line x1="12" y1="17" x2="12" y2="22"/>'
    b'<path d="M5 17h14v-1.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 '
    b'10.76V6h1a2 2 0 0 0 0-4H8a2 2 0 0 0 0 4h1v4.76a2 2 0 0 1-1.11 '
    b'1.79l-1.78.9A2 2 0 0 0 5 15.24Z"/></svg>'
)

SVG_PIN_ON: bytes = (
    b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
    b'fill="#89dfff" stroke="#89dfff" stroke-width="2" stroke-linecap="round" '
    b'stroke-linejoin="round"><line x1="12" y1="17" x2="12" y2="22"/>'
    b'<path d="M5 17h14v-1.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 '
    b'10.76V6h1a2 2 0 0 0 0-4H8a2 2 0 0 0 0 4h1v4.76a2 2 0 0 1-1.11 '
    b'1.79l-1.78.9A2 2 0 0 0 5 15.24Z"/></svg>'
)

SVG_EYE_OPEN: bytes = (
    b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
    b'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    b'stroke-linejoin="round">'
    b'<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>'
    b'<circle cx="12" cy="12" r="3"/></svg>'
)

SVG_EYE_CLOSED: bytes = (
    b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
    b'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    b'stroke-linejoin="round">'
    b'<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8'
    b'a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4'
    b'c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07'
    b'a3 3 0 1 1-4.24-4.24"/>'
    b'<line x1="1" y1="1" x2="23" y2="23"/></svg>'
)

LOGO_B64: str = "AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD///8A////Av///xn///8y////M/7//hf+//4y////N/7//xr///8A/f/9AAAAAAAAAAAA/v//AP7//wz///8z////Mv///xn///8C////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////AP///wT///9q////1/////D////o////Uf///8j////3////lv7//wH///8AAAAAAAAAAAD///8A////OP///+n////w////1////2v///8E////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD///8A////NP///+r/////////8v///8////80////nf/////////V////Gf///wAAAAAAAAAAAP///wD///8x////zv////L/////////6////zb///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP///wD///9i//////////3///9w////E/7//gH///9d/////f////j///9L////APf9+QAAAAAA////AP///wX///8T////cP////3/////////ZP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////AP///2v/////////9v///0H///8A////AP///yX////i/////////43///8A/v//AAAAAAAAAAAAAAAAAP///wD///9A////9v////////9u////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD///8A////a//////////2////QP///wD///8A////Bv///67/////////y////xL///8AAAAAAAAAAAAAAAAA////AP///0D////2/////////27///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP///wD///9r//////////b///9A////AP3+/QD///8A////bP/////////y////Pv///wAAAAAAAAAAAAAAAAD///8A////QP////b/////////bv///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD///8A////AP///3n/////////8P///zb///8AAAAAAP///wD///8w////6v////////9/////AP7//gAAAAAAAAAAAP///wD///81////8P////////98////AP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////AP///y3///+V////3v////7///+v////D////wAAAAAA////AP///wr///+7/////////7////8M////AAAAAAAAAAAA////AP///w////+t/////v///9////+V////Lv///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD///8A////Uf////z/////////1f///zb///8A/v/+AAAAAAD+//4A////AP///3r/////////7P///zP///8AAAAAAAAAAAD+//4A////AP///zT////U//////////z///9S////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP///wD///8r////jv///9v/////////s////xD///8AAAAAAAAAAAD///8A////O/////H/////////cP///wD+//4AAAAAAP///wD///8Q////sv/////////b////jv///yz///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP///wD///8A////d//////////x////Nv///wAAAAAAAAAAAP///wD///8Q////yP////////+y////B////wAAAAAA////AP///zb////w/////////3r///8A////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP///wD///9r//////////b///9A////AAAAAAAAAAAA/v/+AP///wD///+J/////////+X///8o////AAAAAAD///8A////QP////b/////////bv///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////AP///2v/////////9v///0D///8AAAAAAAAAAAAAAAAA////AP///0j////2/////v///2L///8A/f7+AP///wD///9A////9v////////9u////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD///8A////a//////////2////Qf///wAAAAAAAAAAAAAAAAD///8A////F////9P/////////pf7//gP///8A////AP///0H////2/////////27///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP///wD///9h//////////3///90////GP///wb///8AAAAAAP7//gD8//wB////mP/////////c////H////wT///8X////dP////3/////////Y////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////AP///zP////o//////////X////U////M////wAAAAAA/P7+AP///wD///9V////+/////v///9R////L////9T////1/////////+n///80////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD///8A////A////2T////S////7f///+b///84////AAAAAAAAAAAA////AP///x/////Q////9P///4f///83////5f///+3////T////Zv///wP///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD///8A/v/+Af///xb///8s/v/+Lv7//gv+//4AAAAAAAAAAAD+//4A/v/+A/7//ib+//4x/v/+Iv7//gz+//4u////Lf///xb+//4B/v/+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/////////////////////////////////gHwf/wA8D/8APA//ADwP/ww/D/8MHw//Dh8P/w4fD/wODwP8Hw+D/A8PA/8PBw//D4cP/w+HD/8Pgw//A4AP/wPAD/8DwA//g8Af/////////////////////////////////////8="
