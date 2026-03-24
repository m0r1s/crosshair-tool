from __future__ import annotations

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

import base64
import math
from typing import Optional

from PySide6.QtCore import (
    QPoint,
    QPointF,
    QRect,
    QRectF,
    QSize,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QPolygon,
    QRadialGradient,
)
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QDoubleSpinBox,
    QVBoxLayout,
    QWidget,
)

from ..utils.constants import (
    COLOR_PRESETS,
    FONT,
    KNOB_D,
    KNOB_OFF,
    KNOB_TRAV,
    KNOB_Y,
    LOGO_B64,
    SVG_EYE_CLOSED,
    SVG_EYE_OPEN,
    SVG_PIN,
    SVG_PIN_ON,
    SW_H,
    SW_W,
    TRACK_H,
    TRACK_OFF,
    TRACK_ON,
    TRACK_Y,
)


def _svg_icon(svg_bytes: bytes, size: int = 16, color: str = "#52596b") -> QIcon:
    colored = svg_bytes.replace(b"currentColor", color.encode())
    pix = QPixmap()
    pix.loadFromData(colored, "SVG")
    return QIcon(pix.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation))


class ToggleSwitch(QWidget):
    toggled = Signal(bool)

    def __init__(self, checked: bool = False, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._on       = checked
        self._anim_pos = 1.0 if checked else 0.0
        self.setFixedSize(SW_W, SW_H)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._timer = QTimer(self)
        self._timer.setInterval(12)
        self._timer.timeout.connect(self._step)

    def _step(self) -> None:
        target = 1.0 if self._on else 0.0
        diff   = target - self._anim_pos
        if abs(diff) < 0.03:
            self._anim_pos = target
            self._timer.stop()
        else:
            self._anim_pos += diff * 0.22
        self.update()

    def isChecked(self) -> bool:
        return self._on

    def setChecked(self, v: bool, animate: bool = True) -> None:
        if v == self._on:
            return
        self._on = v
        if animate:
            self._timer.start()
        else:
            self._anim_pos = 1.0 if v else 0.0
            self.update()
        self.toggled.emit(v)

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.MouseButton.LeftButton:
            self.setChecked(not self._on)

    def paintEvent(self, _event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        a = self._anim_pos

        c_off, c_on = TRACK_OFF, TRACK_ON
        rv = int(c_off[0] + (c_on[0] - c_off[0]) * a)
        gv = int(c_off[1] + (c_on[1] - c_off[1]) * a)
        bv = int(c_off[2] + (c_on[2] - c_off[2]) * a)

        knob_off_cx = KNOB_OFF + KNOB_D / 2
        knob_on_cx  = KNOB_OFF + KNOB_TRAV + KNOB_D / 2
        track_x     = knob_off_cx - TRACK_H / 2
        track_w     = (knob_on_cx + TRACK_H / 2) - track_x
        track_rect  = QRectF(track_x, TRACK_Y, track_w, TRACK_H)
        radius      = TRACK_H / 2

        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(QColor(rv, gv, bv)))
        p.drawRoundedRect(track_rect, radius, radius)

        knob_x    = KNOB_OFF + self._anim_pos * KNOB_TRAV
        knob_rect = QRectF(knob_x, KNOB_Y, KNOB_D, KNOB_D)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(QColor("#ffffff")))
        p.drawEllipse(knob_rect)
        p.end()


class TitleBar(QWidget):
    pin_toggled        = Signal(bool)
    eye_toggled        = Signal(bool)
    close_requested    = Signal()
    minimize_requested = Signal()

    def __init__(self, win: QWidget, visible: bool = True) -> None:
        super().__init__()
        self.setObjectName("titleBar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedHeight(34)
        self._win    = win
        self._drag: Optional[QPoint] = None
        self._pinned = False
        self._eye_on = visible

        lo = QHBoxLayout(self)
        lo.setContentsMargins(12, 0, 8, 0)
        lo.setSpacing(4)

        logo_lbl = QLabel()
        logo_lbl.setFixedSize(16, 16)
        logo_lbl.setPixmap(self._app_pixmap(16))
        lo.addWidget(logo_lbl)
        lo.addSpacing(4)

        title = QLabel(
            f"moris<span style='color:#89dfff;'>.software</span> / crosshair tool")
        title.setTextFormat(Qt.TextFormat.RichText)
        title.setStyleSheet(
            f"font-family: {FONT}; font-size:11px; font-weight:700; color:#eef0f5;")
        title.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        lo.addWidget(title)
        lo.addStretch()

        self._eye_btn = QPushButton(self)
        self._eye_btn.setObjectName("btnPin")
        self._eye_btn.setFixedSize(22, 22)
        self._eye_btn.setToolTip("Toggle crosshair visibility")
        self._eye_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._eye_btn.clicked.connect(self._toggle_eye)
        self._refresh_eye()
        lo.addWidget(self._eye_btn)

        self._pin_btn = QPushButton(self)
        self._pin_btn.setObjectName("btnPin")
        self._pin_btn.setFixedSize(22, 22)
        self._pin_btn.setIcon(_svg_icon(SVG_PIN, 14, "#52596b"))
        self._pin_btn.setToolTip("Always on top")
        self._pin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._pin_btn.clicked.connect(self._toggle_pin)
        lo.addWidget(self._pin_btn)

        mn = QPushButton(self)
        mn.setObjectName("btnMinimize")
        mn.setFixedSize(22, 22)
        mn.setCursor(Qt.CursorShape.PointingHandCursor)
        mn.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        mn.clicked.connect(win.showMinimized)
        mn.paintEvent = lambda e, b=mn: self._paint_minus(e, b)
        lo.addWidget(mn)

        cl = QPushButton("\u2715", self)
        cl.setObjectName("btnClose")
        cl.setFixedSize(22, 22)
        cl.setCursor(Qt.CursorShape.PointingHandCursor)
        cl.clicked.connect(self.close_requested.emit)
        lo.addWidget(cl)

    @staticmethod
    def _paint_minus(event, btn: QPushButton) -> None:
        QPushButton.paintEvent(btn, event)
        p = QPainter(btn)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor("#ffdc32") if btn.underMouse() else QColor("#52596b")
        p.setPen(QPen(color, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        cx = btn.width() // 2
        cy = btn.height() // 2
        p.drawLine(cx - 3, cy, cx + 3, cy)
        p.end()

    def set_eye(self, visible: bool) -> None:
        self._eye_on = visible
        self._refresh_eye()

    def _refresh_eye(self) -> None:
        if self._eye_on:
            self._eye_btn.setIcon(_svg_icon(SVG_EYE_OPEN, 14, "#52596b"))
        else:
            self._eye_btn.setIcon(_svg_icon(SVG_EYE_CLOSED, 14, "#ff4b69"))

    def _toggle_eye(self) -> None:
        self._eye_on = not self._eye_on
        self._refresh_eye()
        self.eye_toggled.emit(self._eye_on)

    @staticmethod
    def _app_pixmap(size: int) -> QPixmap:
        padded = LOGO_B64 + "=" * (-len(LOGO_B64) % 4)
        data = base64.b64decode(padded)
        pix = QPixmap()
        pix.loadFromData(data, "ICO")
        return pix.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def _toggle_pin(self) -> None:
        self._pinned = not self._pinned
        self._pin_btn.setObjectName("btnPinOn" if self._pinned else "btnPin")
        self._pin_btn.style().unpolish(self._pin_btn)
        self._pin_btn.style().polish(self._pin_btn)
        if self._pinned:
            self._pin_btn.setIcon(_svg_icon(SVG_PIN_ON, 14, "#78c8ff"))
        else:
            self._pin_btn.setIcon(_svg_icon(SVG_PIN, 14, "#52596b"))
        self.pin_toggled.emit(self._pinned)

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag = e.globalPosition().toPoint() - self._win.frameGeometry().topLeft()

    def mouseMoveEvent(self, e) -> None:
        if self._drag and e.buttons() == Qt.MouseButton.LeftButton:
            self._win.move(e.globalPosition().toPoint() - self._drag)

    def mouseReleaseEvent(self, _e) -> None:
        self._drag = None


class CrosshairPreview(QWidget):
    line_clicked = Signal(str)

    def __init__(self, settings: dict, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._s = dict(settings)
        self.setObjectName("previewCard")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedHeight(100)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        lbl = QLabel("PREVIEW", self)
        lbl.setStyleSheet(
            f"font-family:{FONT}; font-size:10px; font-weight:700;"
            " color:#7a8299; letter-spacing:1.4px; background:transparent;")
        lbl.move(12, 10)

    def update_settings(self, s: dict) -> None:
        self._s = dict(s)
        self.update()

    def mousePressEvent(self, e) -> None:
        if e.button() != Qt.MouseButton.LeftButton:
            return
        cx = self.width()  // 2
        cy = self.height() // 2
        dx = e.position().x() - cx
        dy = e.position().y() - cy
        if abs(dx) < abs(dy):
            key = "line_top" if dy < 0 else "line_bottom"
        else:
            key = "line_left" if dx < 0 else "line_right"
        self.line_clicked.emit(key)

    def paintEvent(self, _event) -> None:
        s = self._s
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        cx = self.width()  // 2
        cy = self.height() // 2

        sc     = 2.0
        length = max(2, int(s.get("length",    8) * sc))
        thick  = max(1, int(s.get("thickness", 2) * sc))
        gap    = max(0, int(s.get("gap",        4) * sc))

        color = QColor(s.get("color", "#00FF00"))
        color.setAlpha(max(0, min(255, int(s.get("opacity", 220)))))

        oe = s.get("outline_enabled", False)
        oc = QColor(s.get("outline_color", "#000000"))
        oc.setAlpha(color.alpha())
        ot = max(1, int(s.get("outline_thickness", 1)))

        de = s.get("dot_enabled", False)
        ds = max(1, int(s.get("dot_size", 3) * sc))

        _AR = {"16:9": 16/9, "4:3": 4/3, "5:4": 5/4, "16:10": 16/10}
        _res_ar = _AR.get(s.get("resolution", "16:9"), 16/9)
        hs = (16/9) / _res_ar
        h_thick  = max(1, round(thick  * hs))
        h_gap    = max(0, round(gap    * hs))
        h_length = max(1, round(length * hs))

        def draw(x: int, y: int, w: int, h: int) -> None:
            if oe:
                p.fillRect(x - ot, y - ot, w + ot * 2, h + ot * 2, oc)
            p.fillRect(x, y, w, h, color)

        if s.get("line_top",    True): draw(cx - h_thick//2, cy - gap - length,    h_thick, length)
        if s.get("line_bottom", True): draw(cx - h_thick//2, cy + gap,             h_thick, length)
        if s.get("line_left",   True): draw(cx - h_gap - h_length, cy - thick//2, h_length, thick)
        if s.get("line_right",  True): draw(cx + h_gap,             cy - thick//2, h_length, thick)
        if de:
            dw = max(1, round(ds * hs))
            draw(cx - dw//2, cy - ds//2, dw, ds)
        p.end()


_WHEEL_SIZE  = 200
_RING_W      = 20
_OUTER_R     = _WHEEL_SIZE // 2 - 3
_INNER_R     = _OUTER_R - _RING_W
_SQ_HALF     = int(_INNER_R * 0.65)


class ColorWheelWidget(QWidget):
    color_changed = Signal(str)

    def __init__(self, color: str = "#00FF00", parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setFixedSize(_WHEEL_SIZE, _WHEEL_SIZE)
        self.setCursor(Qt.CursorShape.CrossCursor)
        c = QColor(color)
        h, s, v, _ = c.getHsvF()
        self._h = max(0.0, h)
        self._s = s
        self._v = v
        self._drag: Optional[str] = None

    def color(self) -> str:
        return QColor.fromHsvF(self._h, self._s, self._v).name().upper()

    def set_color(self, hex_str: str) -> None:
        c = QColor(hex_str)
        if not c.isValid():
            return
        h, s, v, _ = c.getHsvF()
        self._h = max(0.0, h)
        self._s = s
        self._v = v
        self.update()

    def _cx(self) -> int: return self.width()  // 2
    def _cy(self) -> int: return self.height() // 2

    def _sq_rect(self) -> QRectF:
        cx, cy = self._cx(), self._cy()
        return QRectF(cx - _SQ_HALF, cy - _SQ_HALF, _SQ_HALF * 2, _SQ_HALF * 2)

    def _ring_pos(self) -> QPointF:
        cx, cy = self._cx(), self._cy()
        angle  = self._h * 2 * math.pi - math.pi / 2
        r      = _INNER_R + _RING_W / 2
        return QPointF(cx + r * math.cos(angle), cy + r * math.sin(angle))

    def _sv_pos(self) -> QPointF:
        sq = self._sq_rect()
        return QPointF(
            sq.left() + self._s * sq.width(),
            sq.top()  + (1.0 - self._v) * sq.height(),
        )

    def paintEvent(self, _event) -> None:
        cx, cy = self._cx(), self._cy()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        grad = QConicalGradient(cx, cy, 90.0)
        for i in range(13):
            t = i / 12.0
            grad.setColorAt(t, QColor.fromHsvF(1.0 - t, 1.0, 1.0))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(grad))
        p.drawEllipse(QPoint(cx, cy), _OUTER_R, _OUTER_R)

        p.setBrush(QColor("#121212"))
        p.drawEllipse(QPoint(cx, cy), _INNER_R - 1, _INNER_R - 1)

        clip = QPainterPath()
        clip.addEllipse(QPointF(cx, cy), float(_INNER_R - 1), float(_INNER_R - 1))
        p.setClipPath(clip)

        sq = self._sq_rect()
        hue_color = QColor.fromHsvF(self._h, 1.0, 1.0)

        sg = QLinearGradient(sq.left(), 0, sq.right(), 0)
        sg.setColorAt(0.0, QColor(255, 255, 255))
        sg.setColorAt(1.0, hue_color)
        p.fillRect(sq, QBrush(sg))

        vg = QLinearGradient(0, sq.top(), 0, sq.bottom())
        vg.setColorAt(0.0, QColor(0, 0, 0, 0))
        vg.setColorAt(1.0, QColor(0, 0, 0, 255))
        p.fillRect(sq, QBrush(vg))

        p.setClipping(False)

        rp = self._ring_pos()
        p.setPen(QPen(QColor(0, 0, 0, 160), 2))
        p.setBrush(hue_color)
        p.drawEllipse(rp, 7.0, 7.0)
        p.setPen(QPen(QColor(255, 255, 255, 200), 1.5))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(rp, 6.5, 6.5)

        sp = self._sv_pos()
        cur_col = QColor.fromHsvF(self._h, self._s, self._v)
        p.setPen(QPen(QColor(0, 0, 0, 160), 1.5))
        p.setBrush(cur_col)
        p.drawEllipse(sp, 5.0, 5.0)
        p.setPen(QPen(QColor(255, 255, 255, 220), 1.5))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(sp, 5.5, 5.5)

        p.end()

    def _dist(self, p: QPointF) -> float:
        return math.hypot(p.x() - self._cx(), p.y() - self._cy())

    def _hit_ring(self, p: QPointF) -> bool:
        d = self._dist(p)
        return _INNER_R - 4 <= d <= _OUTER_R + 4

    def _hit_sq(self, p: QPointF) -> bool:
        return self._sq_rect().contains(p)

    def _set_from_ring(self, p: QPointF) -> None:
        dx = p.x() - self._cx()
        dy = p.y() - self._cy()
        angle = math.atan2(dy, dx) + math.pi / 2
        self._h = (angle / (2 * math.pi)) % 1.0
        self.update()
        self.color_changed.emit(self.color())

    def _set_from_sq(self, p: QPointF) -> None:
        sq = self._sq_rect()
        self._s = max(0.0, min(1.0, (p.x() - sq.left()) / sq.width()))
        self._v = max(0.0, min(1.0, 1.0 - (p.y() - sq.top()) / sq.height()))
        self.update()
        self.color_changed.emit(self.color())

    def mousePressEvent(self, e) -> None:
        pt = QPointF(e.position())
        if self._hit_ring(pt):
            self._drag = "ring"
            self._set_from_ring(pt)
        elif self._hit_sq(pt):
            self._drag = "square"
            self._set_from_sq(pt)

    def mouseMoveEvent(self, e) -> None:
        pt = QPointF(e.position())
        if self._drag == "ring":
            self._set_from_ring(pt)
        elif self._drag == "square":
            self._set_from_sq(pt)

    def mouseReleaseEvent(self, _e) -> None:
        self._drag = None


class LineToggleButton(QPushButton):
    _DIRS = ("up", "down", "left", "right")

    def __init__(self, direction: str, on: bool = True,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        assert direction in self._DIRS
        self._direction = direction
        self.setObjectName("lineBtnOn" if on else "lineBtn")
        self.setFixedSize(20, 20)
        self.setText("")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        on = self.objectName() == "lineBtnOn"
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#89dfff") if on else QColor("#52596b"))

        cx = self.width()  // 2
        cy = self.height() // 2
        w, h = 5, 4

        d = self._direction
        if d == "up":
            pts = [QPoint(cx,     cy - h), QPoint(cx - w, cy + h), QPoint(cx + w, cy + h)]
        elif d == "down":
            pts = [QPoint(cx,     cy + h), QPoint(cx - w, cy - h), QPoint(cx + w, cy - h)]
        elif d == "left":
            pts = [QPoint(cx - h, cy),     QPoint(cx + h, cy - w), QPoint(cx + h, cy + w)]
        else:
            pts = [QPoint(cx + h, cy),     QPoint(cx - h, cy - w), QPoint(cx - h, cy + w)]

        p.drawPolygon(QPolygon(pts))
        p.end()


class HexColorInput(QLineEdit):
    color_changed = Signal(str)

    _SW_W = 22
    _SW_H = 13
    _SW_M = 6

    def __init__(self, color: str = "#00FF00", parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._color = QColor(color if color.startswith("#") else f"#{color}")
        self.setFixedSize(108, 26)
        self.setMaxLength(7)
        self.setTextMargins(self._SW_W + self._SW_M * 2, 0, 0, 0)
        self.setText(self._color.name().upper())
        self.textEdited.connect(self._on_edit)

    def set_color(self, hex_str: str) -> None:
        c = QColor(hex_str)
        if not c.isValid():
            return
        self._color = c
        self.blockSignals(True)
        self.setText(c.name().upper())
        self.blockSignals(False)
        self.update()

    def _on_edit(self, text: str) -> None:
        t = text.strip()
        if not t.startswith("#"):
            t = "#" + t
        if len(t) == 7:
            c = QColor(t)
            if c.isValid():
                self._color = c
                self.update()
                self.color_changed.emit(c.name().upper())

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        sw, sh, sm = self._SW_W, self._SW_H, self._SW_M
        sy = (self.height() - sh) // 2
        p.setPen(QPen(QColor(0, 0, 0, 60), 1))
        p.setBrush(QBrush(self._color))
        p.drawRoundedRect(sm, sy, sw, sh, 3, 3)
        p.end()


class KeyCaptureButton(QPushButton):
    key_captured = Signal(str)

    _MOUSE_BTNS = {
        Qt.MouseButton.LeftButton:    "mouse1",
        Qt.MouseButton.RightButton:   "mouse2",
        Qt.MouseButton.MiddleButton:  "mouse3",
        Qt.MouseButton.BackButton:    "mouse4",
        Qt.MouseButton.ForwardButton: "mouse5",
    }
    _MOUSE_LABELS = {
        "mouse1": "MB1", "mouse2": "MB2", "mouse3": "MB3",
        "mouse4": "MB4", "mouse5": "MB5",
    }

    _SPECIAL: dict = {
        Qt.Key.Key_F1:  "f1",  Qt.Key.Key_F2:  "f2",  Qt.Key.Key_F3:  "f3",
        Qt.Key.Key_F4:  "f4",  Qt.Key.Key_F5:  "f5",  Qt.Key.Key_F6:  "f6",
        Qt.Key.Key_F7:  "f7",  Qt.Key.Key_F8:  "f8",  Qt.Key.Key_F9:  "f9",
        Qt.Key.Key_F10: "f10", Qt.Key.Key_F11: "f11", Qt.Key.Key_F12: "f12",
        Qt.Key.Key_Shift:    "shift",   Qt.Key.Key_Control: "ctrl",
        Qt.Key.Key_Alt:      "alt",     Qt.Key.Key_Tab:     "tab",
        Qt.Key.Key_Return:   "enter",   Qt.Key.Key_Enter:   "enter",
        Qt.Key.Key_Backspace:"backspace",Qt.Key.Key_Delete: "delete",
        Qt.Key.Key_Home:     "home",    Qt.Key.Key_End:     "end",
        Qt.Key.Key_PageUp:   "pageup",  Qt.Key.Key_PageDown:"pagedown",
        Qt.Key.Key_Left:     "left",    Qt.Key.Key_Right:   "right",
        Qt.Key.Key_Up:       "up",      Qt.Key.Key_Down:    "down",
        Qt.Key.Key_Insert:   "insert",  Qt.Key.Key_Space:   "space",
        Qt.Key.Key_CapsLock: "caps_lock",
    }

    def __init__(self, key: str = "", parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._key       = key
        self._capturing = False
        self.setObjectName("btnKey")
        self.setFixedHeight(26)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._refresh()
        self.clicked.connect(self._start)

    def current_key(self) -> str:
        return self._key

    def set_key(self, key: str) -> None:
        self._key = key
        self._refresh()

    def _start(self) -> None:
        self._capturing = True
        self.setText("…")
        self.setFocus()

    def _refresh(self) -> None:
        self._capturing = False
        self.setText(self._MOUSE_LABELS.get(self._key, self._key.upper() if self._key else "None"))

    def mousePressEvent(self, e) -> None:
        if self._capturing:
            name = self._MOUSE_BTNS.get(e.button())
            if name:
                self._key = name
                self.key_captured.emit(name)
                self._refresh()
                e.accept()
                return
        super().mousePressEvent(e)

    def keyPressEvent(self, e) -> None:
        if not self._capturing:
            super().keyPressEvent(e)
            return
        if e.key() == Qt.Key.Key_Escape:
            self._refresh()
            return
        s = self._SPECIAL.get(e.key())
        if s is None:
            t = e.text().lower().strip()
            s = t if t else None
        if s:
            self._key = s
            self.key_captured.emit(s)
        self._refresh()

    def focusOutEvent(self, e) -> None:
        if self._capturing:
            self._refresh()
        super().focusOutEvent(e)


class CustomDropdown(QPushButton):
    option_selected = Signal(str)

    def __init__(
        self,
        options: list[tuple[str, str]],
        current: str = "",
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._options = options
        self._value   = current
        self.setObjectName("btnTypeDropdown")
        self.setFixedHeight(26)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._refresh()
        self.clicked.connect(self._open)

    def sizeHint(self):
        fm = self.fontMetrics()
        max_w = max((fm.horizontalAdvance(l) for l, _ in self._options), default=0)
        from PySide6.QtCore import QSize
        return QSize(10 + max_w + 20, 26)

    def current_value(self) -> str:
        return self._value

    def set_value(self, v: str) -> None:
        self._value = v
        self._refresh()

    def _refresh(self) -> None:
        full = next((l for l, v in self._options if v == self._value), self._value)
        paren = full.find(" (")
        self._label = full[:paren] if paren != -1 else full
        self.setText("")
        self.update()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        p = QPainter(self)
        color = QColor("#eef0f5") if self.underMouse() else QColor("#7a8299")
        p.setPen(color)
        pad = 10
        label = getattr(self, "_label", "")
        p.drawText(
            QRect(pad, 0, self.width() - pad - 18, self.height()),
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
            label,
        )
        p.drawText(
            QRect(0, 0, self.width() - 8, self.height()),
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight,
            "\u25be",
        )
        p.end()

    def _open(self) -> None:
        popup = QWidget(None, Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint
                        | Qt.WindowType.NoDropShadowWindowHint)
        popup.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        outer = QVBoxLayout(popup)
        outer.setContentsMargins(0, 0, 0, 0)

        inner = QFrame()
        inner.setObjectName("typePopupInner")
        inner.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        il = QVBoxLayout(inner)
        il.setContentsMargins(5, 5, 5, 5)
        il.setSpacing(2)

        for label, value in self._options:
            sel = (value == self._value)
            btn = QPushButton(label, inner)
            btn.setObjectName("btnTypeOptionSel" if sel else "btnTypeOption")
            btn.setFixedHeight(26)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(
                lambda _=False, v=value: (self._select(v), popup.close()))
            il.addWidget(btn)

        outer.addWidget(inner)
        inner.setMinimumWidth(self.width())
        gpos = self.mapToGlobal(QPoint(0, self.height() + 3))
        popup.move(gpos)
        popup.show()
        popup.adjustSize()

    def _select(self, value: str) -> None:
        self._value = value
        self._refresh()
        self.option_selected.emit(value)


class _ManualPosOverlay(QWidget):
    confirmed = Signal(int, int)
    closed    = Signal()

    _SNAP = 20

    def __init__(self, sz: int) -> None:
        super().__init__(None)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        self._sz  = sz
        self._sw  = screen.width()
        self._sh  = screen.height()
        self._cx  = screen.width()  // 2
        self._cy  = screen.height() // 2

        self._bx: int = max(0, self._cx - sz // 2)
        self._by: int = max(0, self._cy - sz // 2)
        self._drag_off: Optional[QPoint] = None

    def _box_rect(self) -> QRect:
        return QRect(self._bx, self._by, self._sz, self._sz)

    def _apply_snap(self, bx: int, by: int):
        if abs(bx + self._sz // 2 - self._cx) < self._SNAP:
            bx = self._cx - self._sz // 2
        if abs(by + self._sz // 2 - self._cy) < self._SNAP:
            by = self._cy - self._sz // 2
        return bx, by

    def _is_snapped(self):
        sx = abs(self._bx + self._sz // 2 - self._cx) < self._SNAP
        sy = abs(self._by + self._sz // 2 - self._cy) < self._SNAP
        return sx, sy

    def _stripe_pen(self, color: tuple, offset: float, width: float = 2.0) -> QPen:
        pen = QPen(QColor(*color), width, Qt.PenStyle.CustomDashLine)
        pen.setDashPattern([7.0, 7.0])
        pen.setDashOffset(offset)
        return pen

    @staticmethod
    def _center_offset(center: int, pen_width: float = 2.0) -> float:
        return float((10.5 - center / pen_width) % 14.0)

    def paintEvent(self, _) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        sx, sy = self._is_snapped()

        for vertical, snapped in ((True, sx), (False, sy)):
            snap_col = (255, 215, 50, 240)
            base_col = (255, 255, 255, 160)
            hi_col   = snap_col if snapped else base_col

            center   = self._cy if vertical else self._cx
            d_off    = self._center_offset(center)
            l_off    = (d_off + 7.0) % 14.0

            x1, y1, x2, y2 = (
                (self._cx, 0, self._cx, self._sh) if vertical
                else (0, self._cy, self._sw, self._cy)
            )
            p.setPen(self._stripe_pen((20, 20, 20, 200), d_off))
            p.drawLine(x1, y1, x2, y2)
            p.setPen(self._stripe_pen(hi_col, l_off))
            p.drawLine(x1, y1, x2, y2)

        p.setPen(QPen(QColor(220, 50, 50), 2))
        p.setBrush(QBrush(QColor(220, 50, 50, 45)))
        p.drawRect(self._box_rect())

        hint = "Drag to position   •   Enter or click Done to confirm   •   Esc to cancel"
        p.setPen(QColor(0, 0, 0, 140))
        p.drawText(QRect(0, 18, self._sw, 24), Qt.AlignmentFlag.AlignHCenter, hint)
        p.setPen(QColor(255, 255, 255, 210))
        p.drawText(QRect(0, 17, self._sw, 24), Qt.AlignmentFlag.AlignHCenter, hint)

        p.end()

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.MouseButton.LeftButton:
            pos = e.position().toPoint()
            if self._box_rect().contains(pos):
                self._drag_off = pos - QPoint(self._bx, self._by)
                self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseMoveEvent(self, e) -> None:
        pos = e.position().toPoint()
        if self._drag_off is not None:
            bx = max(0, min(pos.x() - self._drag_off.x(), self._sw - self._sz))
            by = max(0, min(pos.y() - self._drag_off.y(), self._sh - self._sz))
            self._bx, self._by = self._apply_snap(bx, by)
            self.update()
        else:
            if self._box_rect().contains(pos):
                self.setCursor(Qt.CursorShape.OpenHandCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)

    def mouseReleaseEvent(self, e) -> None:
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_off = None
            pos = e.position().toPoint()
            self.setCursor(
                Qt.CursorShape.OpenHandCursor if self._box_rect().contains(pos)
                else Qt.CursorShape.ArrowCursor
            )

    def keyPressEvent(self, e) -> None:
        if e.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.confirm()
        elif e.key() == Qt.Key.Key_Escape:
            self.close()

    def confirm(self) -> None:
        self.confirmed.emit(self._bx, self._by)
        self.close()

    def closeEvent(self, e) -> None:
        self.closed.emit()
        super().closeEvent(e)
