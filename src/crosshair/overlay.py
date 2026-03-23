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

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QApplication, QWidget

if sys.platform == "win32":
    import ctypes

    _HWND_TOPMOST      = -1
    _SWP_NOMOVE        = 0x0002
    _SWP_NOSIZE        = 0x0001
    _SWP_NOACTIVATE    = 0x0010
    _GWL_EXSTYLE       = -20
    _WS_EX_LAYERED     = 0x00080000
    _WS_EX_TRANSPARENT = 0x00000020


class CrosshairOverlay(QWidget):
    def __init__(self, settings: dict) -> None:
        super().__init__(None)
        self._settings: dict = dict(settings)
        self._force_hidden: bool = False

        flags = (
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self._resize_to_screen()

        self._res_timer = QTimer(self)
        self._res_timer.setInterval(1000)
        self._res_timer.timeout.connect(self._resize_to_screen)
        self._res_timer.start()

    def show_overlay(self) -> None:
        self.show()
        if sys.platform == "win32":
            self._apply_win32_flags()

    def apply_settings(self, settings: dict) -> None:
        self._settings = dict(settings)
        self.update()

    def set_visible(self, visible: bool) -> None:
        self._settings["visible"] = visible
        self.update()

    def set_force_hidden(self, hidden: bool) -> None:
        self._force_hidden = hidden
        self.update()

    def _resize_to_screen(self) -> None:
        screen = QApplication.primaryScreen().geometry()
        if self.geometry() != screen:
            self.setGeometry(screen)

    def _apply_win32_flags(self) -> None:
        hwnd = int(self.winId())
        ctypes.windll.user32.SetWindowPos(
            hwnd, _HWND_TOPMOST, 0, 0, 0, 0,
            _SWP_NOMOVE | _SWP_NOSIZE | _SWP_NOACTIVATE,
        )
        ex = ctypes.windll.user32.GetWindowLongW(hwnd, _GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(
            hwnd, _GWL_EXSTYLE,
            ex | _WS_EX_LAYERED | _WS_EX_TRANSPARENT,
        )

    def paintEvent(self, _event) -> None:
        s = self._settings
        if self._force_hidden or not s.get("visible", True):
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        cx = self.width()  // 2
        cy = self.height() // 2

        length = max(1, int(s.get("length", 8)))
        thick  = max(1, int(s.get("thickness", 2)))
        gap    = max(0, int(s.get("gap", 4)))

        color = QColor(s.get("color", "#00FF00"))
        color.setAlpha(max(0, min(255, int(s.get("opacity", 220)))))

        outline_en    = s.get("outline_enabled", False)
        outline_color = QColor(s.get("outline_color", "#000000"))
        outline_color.setAlpha(color.alpha())
        ot = max(1, int(s.get("outline_thickness", 1)))

        dot_en   = s.get("dot_enabled", False)
        dot_size = max(1, int(s.get("dot_size", 3)))

        line_top    = s.get("line_top",    True)
        line_bottom = s.get("line_bottom", True)
        line_left   = s.get("line_left",   True)
        line_right  = s.get("line_right",  True)

        def draw_rect(x: int, y: int, w: int, h: int) -> None:
            if outline_en:
                painter.fillRect(x - ot, y - ot, w + ot * 2, h + ot * 2, outline_color)
            painter.fillRect(x, y, w, h, color)

        if line_top:
            draw_rect(cx - thick // 2, cy - gap - length, thick, length)
        if line_bottom:
            draw_rect(cx - thick // 2, cy + gap,          thick, length)
        if line_left:
            draw_rect(cx - gap - length, cy - thick // 2, length, thick)
        if line_right:
            draw_rect(cx + gap,          cy - thick // 2, length, thick)

        if dot_en:
            ds = dot_size
            draw_rect(cx - ds // 2, cy - ds // 2, ds, ds)

        painter.end()
