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
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

if sys.platform == "win32":
    import ctypes
    _HWND_TOPMOST   = -1
    _SWP_NOMOVE     = 0x0002
    _SWP_NOSIZE     = 0x0001
    _SWP_NOACTIVATE = 0x0010


class ZoomOverlay(QWidget):
    def __init__(self, settings: dict) -> None:
        super().__init__(None)
        self._settings: dict = dict(settings)
        self._active: bool = False

        flags = (
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self._label = QLabel(self)
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setStyleSheet("background: transparent; border: none;")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(2, 2, 2, 2)
        lay.setSpacing(0)
        lay.addWidget(self._label)

        self.setStyleSheet(
            "ZoomOverlay {"
            " background: #0a0a0a;"
            " border: 2px solid rgba(137,223,255,0.35);"
            " border-radius: 8px; }"
        )

        self._timer = QTimer(self)
        self._timer.setInterval(16)
        self._timer.timeout.connect(self._update)

        self._apply_geometry()

    def apply_settings(self, settings: dict) -> None:
        self._settings = dict(settings)
        self._apply_geometry()

    def start_zoom(self) -> None:
        if self._active:
            return
        self._active = True
        sz = max(80, int(self._settings.get("zoom_size", 300)))
        self.setFixedSize(sz, sz)
        self.show()
        if sys.platform == "win32":
            self._set_topmost()
        self._reposition(sz)
        self._timer.start()

    def stop_zoom(self) -> None:
        if not self._active:
            return
        self._active = False
        self._timer.stop()
        if sys.platform == "win32":
            try:
                hwnd = int(self.winId())
                ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 0)
            except Exception:
                pass
        self.hide()

    def toggle_zoom(self) -> None:
        self.stop_zoom() if self._active else self.start_zoom()

    def _apply_geometry(self) -> None:
        sz = max(80, int(self._settings.get("zoom_size", 300)))
        self.setFixedSize(sz, sz)
        self._reposition(sz)

    def _reposition(self, sz: int) -> None:
        s      = self._settings
        anchor = s.get("zoom_anchor", "below")
        screen = QApplication.primaryScreen().geometry()
        cx     = screen.width()  // 2
        cy     = screen.height() // 2

        factor   = max(1.0, float(s.get("zoom_factor", 3.0)))
        cap_half = max(10, int(sz / factor)) // 2 + 12

        if anchor == "below":
            x, y = cx - sz // 2, cy + cap_half
        elif anchor == "above":
            x, y = cx - sz // 2, cy - sz - cap_half
        elif anchor == "left":
            x, y = cx - sz - cap_half, cy - sz // 2
        elif anchor == "right":
            x, y = cx + cap_half, cy - sz // 2
        elif anchor == "middle":
            x, y = cx - sz // 2, cy - sz // 2
        else:
            x = int(s.get("zoom_x", 0))
            y = int(s.get("zoom_y", 0))

        screen_rect = QApplication.primaryScreen().geometry()
        x = max(0, min(x, screen_rect.width()  - sz))
        y = max(0, min(y, screen_rect.height() - sz))
        self.move(x, y)

    def _set_topmost(self) -> None:
        hwnd = int(self.winId())
        ctypes.windll.user32.SetWindowPos(
            hwnd, _HWND_TOPMOST, 0, 0, 0, 0,
            _SWP_NOMOVE | _SWP_NOSIZE | _SWP_NOACTIVATE,
        )
        GWL_EXSTYLE       = -20
        WS_EX_LAYERED     = 0x00080000
        WS_EX_TRANSPARENT = 0x00000020
        ex = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex | WS_EX_LAYERED | WS_EX_TRANSPARENT)
        WDA_EXCLUDEFROMCAPTURE = 0x00000011
        ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)

    def _update(self) -> None:
        s      = self._settings
        sz     = max(80, int(s.get("zoom_size",   300)))
        factor = max(1.0, float(s.get("zoom_factor", 3.0)))
        cap    = max(10, int(sz / factor))

        screen = QApplication.primaryScreen()
        sg     = screen.geometry()
        cx     = sg.width()  // 2
        cy     = sg.height() // 2

        px = screen.grabWindow(
            0,
            cx - cap // 2,
            cy - cap // 2,
            cap,
            cap,
        )
        if px.isNull():
            return

        inner = sz - 4
        scaled = px.scaled(
            inner, inner,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation,
        )
        self._label.setPixmap(scaled)
