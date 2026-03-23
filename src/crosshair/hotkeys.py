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

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QObject, Signal

try:
    from pynput import keyboard as _kb, mouse as _mouse
    _PYNPUT_OK = True
except ImportError:
    _PYNPUT_OK = False


class HotkeySignals(QObject):
    zoom_press          = Signal()
    zoom_release        = Signal()
    toggle_visibility   = Signal()
    right_click_press   = Signal()
    right_click_release = Signal()


class HotkeyManager:
    def __init__(self) -> None:
        self.signals = HotkeySignals()
        self._kb_listener:    Optional[object] = None
        self._mouse_listener: Optional[object] = None
        self._zoom_key:       Optional[str] = None
        self._toggle_key:     Optional[str] = None
        self._zoom_enabled:   bool = True
        self._rc_hide:        bool = True
        self._held: set[str] = set()

    def configure(self, settings: dict) -> None:
        z = settings.get("zoom_hotkey", "").strip().lower()
        t = settings.get("toggle_hotkey", "").strip().lower()
        self._zoom_key     = z if z else None
        self._toggle_key   = t if t else None
        self._zoom_enabled = bool(settings.get("zoom_enabled", True))
        self._rc_hide      = bool(settings.get("right_click_hide", True))

    def start(self) -> None:
        if not _PYNPUT_OK:
            return
        self._start_keyboard()
        self._start_mouse()

    def stop(self) -> None:
        if self._kb_listener:
            try:
                self._kb_listener.stop()
            except Exception:
                pass
            self._kb_listener = None
        if self._mouse_listener:
            try:
                self._mouse_listener.stop()
            except Exception:
                pass
            self._mouse_listener = None
        self._held.clear()

    def restart(self) -> None:
        self.stop()
        self.start()

    @staticmethod
    def _key_str(key) -> str:
        try:
            ch = key.char
            return ch.lower() if ch else ""
        except AttributeError:
            return str(key).replace("Key.", "").lower()

    def _start_keyboard(self) -> None:
        signals = self.signals

        def on_press(key):
            s = HotkeyManager._key_str(key)
            if s in self._held:
                return
            self._held.add(s)
            if self._zoom_enabled and s == self._zoom_key:
                signals.zoom_press.emit()
            if s == self._toggle_key:
                signals.toggle_visibility.emit()

        def on_release(key):
            s = HotkeyManager._key_str(key)
            self._held.discard(s)
            if self._zoom_enabled and s == self._zoom_key:
                signals.zoom_release.emit()

        self._kb_listener = _kb.Listener(
            on_press=on_press,
            on_release=on_release,
            suppress=False,
        )
        self._kb_listener.daemon = True
        self._kb_listener.start()

    def _start_mouse(self) -> None:
        signals = self.signals

        _BTN_MAP = {
            _mouse.Button.left:   "mouse1",
            _mouse.Button.right:  "mouse2",
            _mouse.Button.middle: "mouse3",
        }
        try:
            _BTN_MAP[_mouse.Button.x1] = "mouse4"
            _BTN_MAP[_mouse.Button.x2] = "mouse5"
        except AttributeError:
            pass

        def on_click(x, y, button, pressed):
            bname = _BTN_MAP.get(button, "")

            if bname and self._zoom_enabled and bname == self._zoom_key:
                if pressed and bname not in self._held:
                    self._held.add(bname)
                    signals.zoom_press.emit()
                elif not pressed and bname in self._held:
                    self._held.discard(bname)
                    signals.zoom_release.emit()
                return

            if bname and pressed and bname == self._toggle_key:
                signals.toggle_visibility.emit()
                return

            if button == _mouse.Button.right and self._rc_hide:
                if pressed:
                    signals.right_click_press.emit()
                else:
                    signals.right_click_release.emit()

        self._mouse_listener = _mouse.Listener(
            on_click=on_click,
            suppress=False,
        )
        self._mouse_listener.daemon = True
        self._mouse_listener.start()
