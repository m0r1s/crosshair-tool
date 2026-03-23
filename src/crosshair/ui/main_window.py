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

import os
from copy import deepcopy
from typing import Optional

from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QDoubleSpinBox,
    QVBoxLayout,
    QWidget,
)

from ..hotkeys import HotkeyManager
from ..overlay import CrosshairOverlay
from ..utils.constants import APP_NAME, APP_VERSION, COLOR_PRESETS, FONT
from ..utils.settings import export_profile, import_profile, save_settings
from ..zoom_overlay import ZoomOverlay
from .widgets import (
    ColorWheelWidget,
    CrosshairPreview,
    CustomDropdown,
    HexColorInput,
    KeyCaptureButton,
    TitleBar,
    ToggleSwitch,
    _ManualPosOverlay,
)


class _NoScrollSpin(QSpinBox):
    def wheelEvent(self, e) -> None:
        e.ignore()

class _NoScrollDSpin(QDoubleSpinBox):
    def wheelEvent(self, e) -> None:
        e.ignore()


class MainWindow(QWidget):
    def __init__(
        self,
        overlay: CrosshairOverlay,
        zoom: ZoomOverlay,
        hotkeys: HotkeyManager,
        settings: dict,
        profiles: dict,
    ) -> None:
        super().__init__(None)
        self._overlay  = overlay
        self._zoom     = zoom
        self._hotkeys  = hotkeys
        self._s        = dict(settings)
        self._profiles = dict(profiles)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self._build()
        self.setFixedWidth(380)

    def _build(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)

        container = QWidget()
        container.setObjectName("mainContainer")
        container.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 200))
        shadow.setOffset(0, 10)
        container.setGraphicsEffect(shadow)
        root.addWidget(container)

        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        tb = TitleBar(self, visible=self._s.get("visible", True))
        tb.pin_toggled.connect(self._on_pin)
        tb.eye_toggled.connect(self._on_vis_toggle)
        tb.close_requested.connect(self._quit)
        self._title_bar = tb
        vbox.addWidget(tb)

        vbox.addWidget(self._sep())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        body = QWidget()
        body.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)
        bl = QVBoxLayout(body)
        bl.setContentsMargins(12, 10, 12, 10)
        bl.setSpacing(8)

        self._build_preview(bl)
        self._build_crosshair_card(bl)
        self._build_color_card(bl)
        self._build_visibility_card(bl)
        self._build_zoom_card(bl)
        self._build_profiles_card(bl)
        self._build_links_card(bl)
        bl.addStretch()

        scroll.setWidget(body)
        scroll.setFixedHeight(480)
        vbox.addWidget(scroll)

        footer_widget = QWidget()
        footer_widget.setObjectName("statusBar")
        footer_widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        footer = QHBoxLayout(footer_widget)
        footer.setContentsMargins(10, 4, 10, 5)
        lc = QLabel("Made with \u2665 by moris and tim")
        lc.setStyleSheet(f"font-family:{FONT}; font-size:10px; color:#3a3f4d;")
        lv = QLabel("v2.1.0")
        lv.setStyleSheet(f"font-family:{FONT}; font-size:10px; color:#3a3f4d;")
        footer.addWidget(lc)
        footer.addStretch()
        footer.addWidget(lv)
        vbox.addWidget(footer_widget)

    @staticmethod
    def _card() -> QWidget:
        w = QWidget()
        w.setObjectName("settingsCard")
        w.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        return w

    @staticmethod
    def _cap(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet(
            f"font-family:{FONT}; font-size:10px; font-weight:700;"
            " color:#7a8299; letter-spacing:1.4px;")
        return lbl

    @staticmethod
    def _muted(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet(f"font-family:{FONT}; font-size:11px; color:#7a8299;")
        return lbl

    @staticmethod
    def _sep() -> QFrame:
        f = QFrame()
        f.setObjectName("sep")
        f.setFixedHeight(1)
        return f

    def _row(self, label: str, *widgets: QWidget) -> QHBoxLayout:
        h = QHBoxLayout()
        h.setSpacing(8)
        h.setContentsMargins(0, 0, 0, 0)
        h.addWidget(self._muted(label))
        h.addStretch()
        for w in widgets:
            h.addWidget(w)
        return h

    def _toggle_row(self, label: str, switch: ToggleSwitch) -> QHBoxLayout:
        h = QHBoxLayout()
        h.setSpacing(10)
        h.setContentsMargins(0, 0, 0, 0)
        h.addWidget(switch, 0, Qt.AlignmentFlag.AlignVCenter)
        lbl = QLabel(label)
        lbl.setStyleSheet(f"font-family:{FONT}; font-size:12px; color:#eef0f5;")
        h.addWidget(lbl, 0, Qt.AlignmentFlag.AlignVCenter)
        h.addStretch()
        return h

    @staticmethod
    def _spin(value: int, lo: int, hi: int, w: int = 60) -> QSpinBox:
        sb = _NoScrollSpin()
        sb.setRange(lo, hi)
        sb.setValue(value)
        sb.setFixedSize(w, 26)
        return sb

    @staticmethod
    def _dspin(value: float, lo: float, hi: float, step: float = 0.5, w: int = 60) -> QDoubleSpinBox:
        sb = _NoScrollDSpin()
        sb.setRange(lo, hi)
        sb.setValue(value)
        sb.setSingleStep(step)
        sb.setDecimals(1)
        sb.setFixedSize(w, 26)
        return sb

    def _build_preview(self, parent: QVBoxLayout) -> None:
        self._preview = CrosshairPreview(self._s)
        self._preview.line_clicked.connect(self._toggle_line)
        parent.addWidget(self._preview)

    def _build_crosshair_card(self, parent: QVBoxLayout) -> None:
        card = self._card()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(12, 10, 12, 10)
        cl.setSpacing(7)
        cl.addWidget(self._cap("CROSSHAIR"))

        self._sp_len   = self._spin(self._s.get("length",    8), 1, 200, 52)
        self._sp_thick = self._spin(self._s.get("thickness", 2), 1,  50, 52)
        self._sp_gap   = self._spin(self._s.get("gap",       4), 0, 100, 52)
        self._sp_len.valueChanged.connect(   lambda v: self._set("length",    v))
        self._sp_thick.valueChanged.connect( lambda v: self._set("thickness", v))
        self._sp_gap.valueChanged.connect(   lambda v: self._set("gap",       v))
        size_row = QHBoxLayout()
        size_row.setSpacing(6)
        size_row.setContentsMargins(0, 0, 0, 0)
        for lbl, sp in [("Length", self._sp_len), ("Thickness", self._sp_thick)]:
            size_row.addWidget(self._muted(lbl))
            size_row.addWidget(sp)
            size_row.addSpacing(6)
        size_row.addStretch()
        size_row.addWidget(self._muted("Gap"))
        size_row.addWidget(self._sp_gap)
        cl.addLayout(size_row)

        cl.addWidget(self._sep())

        self._sw_outline = ToggleSwitch(self._s.get("outline_enabled", False))
        self._sw_outline.toggled.connect(lambda v: self._set("outline_enabled", v))
        out_row = self._toggle_row("Outline", self._sw_outline)
        self._sp_out_thick = self._spin(self._s.get("outline_thickness", 1), 1, 10, 52)
        self._sp_out_thick.valueChanged.connect(lambda v: self._set("outline_thickness", v))
        out_row.addWidget(self._muted("Thickness"))
        out_row.addWidget(self._sp_out_thick)
        cl.addLayout(out_row)

        self._sw_dot = ToggleSwitch(self._s.get("dot_enabled", False))
        self._sw_dot.toggled.connect(lambda v: self._set("dot_enabled", v))
        dot_row = self._toggle_row("Center dot", self._sw_dot)
        self._sp_dot = self._spin(self._s.get("dot_size", 3), 1, 20, 52)
        self._sp_dot.valueChanged.connect(lambda v: self._set("dot_size", v))
        dot_row.addWidget(self._muted("Size"))
        dot_row.addWidget(self._sp_dot)
        cl.addLayout(dot_row)

        parent.addWidget(card)

    def _toggle_line(self, key: str) -> None:
        self._set(key, not self._s.get(key, True))

    def _build_color_card(self, parent: QVBoxLayout) -> None:
        card = self._card()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(12, 10, 12, 10)
        cl.setSpacing(8)

        cl.addWidget(self._cap("COLOR"))

        self._color_target = "crosshair"
        self._dd_color_target = CustomDropdown(
            [("Crosshair", "crosshair"), ("Outline", "outline")],
            "crosshair",
        )
        self._dd_color_target.setParent(card)
        self._dd_color_target.option_selected.connect(self._on_color_target_change)
        from PySide6.QtCore import QTimer as _QTimer
        _QTimer.singleShot(0, lambda: (
            self._dd_color_target.adjustSize(),
            self._dd_color_target.move(
                card.width() - self._dd_color_target.width() - 12,
                10,
            ),
            self._dd_color_target.raise_(),
            self._dd_color_target.show(),
        ))

        _SWATCHES = ["#FF0000", "#FFA500", "#FFFF00", "#00FF00",
                     "#00FFFF", "#0000FF", "#FFFFFF", "#000000"]
        _SW = 18; _GAP = 4
        _swatch_btns = []
        for hex_str in _SWATCHES:
            btn = QPushButton(card)
            btn.setFixedSize(_SW, _SW)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(
                f"QPushButton {{ background:{hex_str};"
                f" border:1px solid rgba(255,255,255,0.15); border-radius:3px; }}"
                f"QPushButton:hover {{ border:1px solid rgba(255,255,255,0.65); }}"
            )
            btn.raise_()
            btn.show()
            btn.clicked.connect(lambda _=False, h=hex_str: self._apply_color(h))
            _swatch_btns.append(btn)

        def _place_swatches():
            total_h = len(_swatch_btns) * _SW + (len(_swatch_btns) - 1) * _GAP
            y0 = (card.height() - total_h) // 2
            for idx, b in enumerate(_swatch_btns):
                b.move(8, y0 + idx * (_SW + _GAP))
        QTimer.singleShot(0, _place_swatches)

        self._wheel = ColorWheelWidget(self._s.get("color", "#00FF00"))
        self._wheel.color_changed.connect(self._on_wheel_color)

        wh_row = QHBoxLayout()
        wh_row.addStretch()
        wh_row.addWidget(self._wheel)
        wh_row.addStretch()
        cl.addLayout(wh_row)

        hex_row = QHBoxLayout()
        hex_row.setSpacing(8)
        self._hex_edit = HexColorInput(self._s.get("color", "#00FF00"))
        self._hex_edit.color_changed.connect(self._on_hex_edit)
        hex_row.addWidget(self._hex_edit)
        hex_row.addStretch()
        hex_row.addWidget(self._muted("Opacity"))
        self._sp_opacity = self._spin(self._s.get("opacity", 220), 0, 999, 65)
        self._sp_opacity.valueChanged.connect(
            lambda v: self._sp_opacity.setValue(255) if v > 255 else self._set("opacity", v)
        )
        hex_row.addWidget(self._sp_opacity)
        cl.addLayout(hex_row)

        parent.addWidget(card)

    def _on_color_target_change(self, target: str) -> None:
        self._color_target = target
        if target == "crosshair":
            self._apply_color(self._s.get("color", "#00FF00"), from_target=True)
        else:
            self._apply_outline_color(self._s.get("outline_color", "#000000"), from_target=True)

    def _on_wheel_color(self, hex_str: str) -> None:
        if self._color_target == "crosshair":
            self._apply_color(hex_str)
        else:
            self._apply_outline_color(hex_str)

    def _on_hex_edit(self, hex_str: str) -> None:
        if self._color_target == "crosshair":
            self._apply_color(hex_str)
        else:
            self._apply_outline_color(hex_str)

    def _apply_color(self, hex_str: str, from_target: bool = False) -> None:
        self._set("color", hex_str)
        self._wheel.set_color(hex_str)
        self._hex_edit.set_color(hex_str)

    def _apply_outline_color(self, hex_str: str, from_target: bool = False) -> None:
        if not from_target:
            self._set("outline_color", hex_str)
        self._wheel.set_color(hex_str)
        self._hex_edit.set_color(hex_str)

    def _build_visibility_card(self, parent: QVBoxLayout) -> None:
        card = self._card()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(12, 10, 12, 10)
        cl.setSpacing(7)
        cl.addWidget(self._cap("VISIBILITY"))

        self._sw_vis = ToggleSwitch(self._s.get("visible", True))
        self._sw_vis.toggled.connect(self._on_vis_toggle)
        self._btn_toggle_key = KeyCaptureButton(self._s.get("toggle_hotkey", ""))
        self._btn_toggle_key.setFixedWidth(65)
        self._btn_toggle_key.key_captured.connect(
            lambda k: self._on_key_captured("toggle_hotkey", k, self._btn_toggle_key))
        vis_row = self._toggle_row("Crosshair visible", self._sw_vis)
        vis_row.addWidget(self._btn_toggle_key)
        cl.addLayout(vis_row)

        cl.addWidget(self._sep())

        self._sw_rc = ToggleSwitch(self._s.get("right_click_hide", True))
        self._sw_rc.toggled.connect(lambda v: self._set("right_click_hide", v))
        self._dd_rc_mode = CustomDropdown(
            [("Hold (hide while held)", "hold"),
             ("Toggle (click to toggle)", "toggle")],
            self._s.get("right_click_mode", "hold"),
        )
        self._dd_rc_mode.setFixedWidth(65)
        self._dd_rc_mode.option_selected.connect(lambda v: self._set("right_click_mode", v))
        rc_row = self._toggle_row("Hide on right-click", self._sw_rc)
        rc_row.addWidget(self._dd_rc_mode)
        cl.addLayout(rc_row)

        parent.addWidget(card)

    def _build_zoom_card(self, parent: QVBoxLayout) -> None:
        card = self._card()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(12, 10, 12, 10)
        cl.setSpacing(7)
        cl.addWidget(self._cap("ZOOM"))

        self._sw_zoom = ToggleSwitch(self._s.get("zoom_enabled", True))
        self._sw_zoom.toggled.connect(lambda v: self._set("zoom_enabled", v))
        self._btn_zoom_key = KeyCaptureButton(self._s.get("zoom_hotkey", "c"))
        self._btn_zoom_key.setFixedWidth(65)
        self._btn_zoom_key.key_captured.connect(
            lambda k: self._on_key_captured("zoom_hotkey", k, self._btn_zoom_key))
        zoom_row = self._toggle_row("Enable zoom", self._sw_zoom)
        zoom_row.addWidget(self._btn_zoom_key)
        cl.addLayout(zoom_row)

        self._dd_zoom_mode = CustomDropdown(
            [("Hold (show while held)", "hold"),
             ("Toggle (click to toggle)", "toggle")],
            self._s.get("zoom_mode", "hold"),
        )
        self._dd_zoom_mode.setFixedWidth(65)
        self._dd_zoom_mode.option_selected.connect(lambda v: self._set("zoom_mode", v))
        cl.addLayout(self._row("Trigger mode", self._dd_zoom_mode))

        cl.addWidget(self._sep())

        self._sp_factor = self._dspin(self._s.get("zoom_factor", 3.0), 1.0, 20.0, w=65)
        self._sp_factor.valueChanged.connect(lambda v: self._set("zoom_factor", v))
        cl.addLayout(self._row("Zoom factor", self._sp_factor))

        self._sp_zoom_sz = self._spin(self._s.get("zoom_size", 300), 80, 800, 65)
        self._sp_zoom_sz.valueChanged.connect(lambda v: self._set("zoom_size", v))
        cl.addLayout(self._row("Window size (px)", self._sp_zoom_sz))

        cl.addWidget(self._sep())

        self._dd_anchor = CustomDropdown(
            [("Below",  "below"),
             ("Above",  "above"),
             ("Left",   "left"),
             ("Right",  "right"),
             ("Middle", "middle"),
             ("Set",    "set")],
            self._s.get("zoom_anchor", "below"),
        )
        self._dd_anchor.setFixedWidth(65)
        self._dd_anchor.option_selected.connect(self._on_anchor)
        cl.addLayout(self._row("Position anchor", self._dd_anchor))

        self._custom_xy = QWidget()
        xy_lay = QVBoxLayout(self._custom_xy)
        xy_lay.setContentsMargins(0, 0, 0, 0)
        xy_lay.setSpacing(7)
        self._sp_zoom_x = self._spin(self._s.get("zoom_x", 0), 0, 7680, 65)
        self._sp_zoom_y = self._spin(self._s.get("zoom_y", 0), 0, 4320, 65)
        self._sp_zoom_x.valueChanged.connect(lambda v: self._set("zoom_x", v))
        self._sp_zoom_y.valueChanged.connect(lambda v: self._set("zoom_y", v))
        xy_lay.addLayout(self._row("X position", self._sp_zoom_x))
        xy_lay.addLayout(self._row("Y position", self._sp_zoom_y))
        xy_lay.addSpacing(2)
        self._btn_set_manually = QPushButton("Set Position Manually")
        self._btn_set_manually.setObjectName("btnNeutral")
        self._btn_set_manually.setFixedHeight(26)
        self._btn_set_manually.clicked.connect(self._toggle_manual_pos)
        xy_lay.addWidget(self._btn_set_manually)
        self._manual_overlay: _ManualPosOverlay = None
        self._custom_xy.setVisible(self._s.get("zoom_anchor", "below") == "set")
        cl.addWidget(self._custom_xy)

        parent.addWidget(card)

    def _on_anchor(self, value: str) -> None:
        self._set("zoom_anchor", value)
        self._custom_xy.setVisible(value == "set")

    def _toggle_manual_pos(self) -> None:
        if self._manual_overlay is not None:
            self._manual_overlay.confirm()
            return
        sz = max(80, int(self._s.get("zoom_size", 300)))
        ov = _ManualPosOverlay(sz)
        ov.confirmed.connect(self._on_manual_pos_confirmed)
        ov.closed.connect(self._on_manual_overlay_closed)
        self._manual_overlay = ov
        self._btn_set_manually.setText("Done  ↵")
        ov.show()
        ov.activateWindow()
        ov.setFocus()

    def _on_manual_pos_confirmed(self, x: int, y: int) -> None:
        self._sp_zoom_x.setValue(x)
        self._sp_zoom_y.setValue(y)
        self._set("zoom_x", x)
        self._set("zoom_y", y)

    def _on_manual_overlay_closed(self) -> None:
        self._manual_overlay = None
        self._btn_set_manually.setText("Set Position Manually")

    def _build_profiles_card(self, parent: QVBoxLayout) -> None:
        card = self._card()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(12, 10, 12, 10)
        cl.setSpacing(7)
        cl.addWidget(self._cap("PROFILES"))

        self._profile_list = QListWidget()
        self._profile_list.setFixedHeight(110)
        self._profile_list.currentTextChanged.connect(
            lambda t: self._prof_name.setText(t))
        cl.addWidget(self._profile_list)

        name_row = QHBoxLayout()
        name_row.setSpacing(6)
        name_row.addWidget(self._muted("Name"))
        self._prof_name = QLineEdit()
        self._prof_name.setPlaceholderText("profile name…")
        name_row.addWidget(self._prof_name)
        cl.addLayout(name_row)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)
        for label, obj, fn in [
            ("Save",   "btnPrimary", self._prof_save),
            ("Load",   "btnNeutral", self._prof_load),
            ("Delete", "btnDanger",  self._prof_del),
        ]:
            b = QPushButton(label)
            b.setObjectName(obj)
            b.setFixedHeight(28)
            b.clicked.connect(fn)
            btn_row.addWidget(b)
        cl.addLayout(btn_row)

        cl.addWidget(self._sep())

        io_row = QHBoxLayout()
        io_row.setSpacing(6)
        for label, obj, fn in [
            ("\u2193  Export JSON", "btnNeutral", self._prof_export),
            ("\u2191  Import JSON", "btnPrimary", self._prof_import),
        ]:
            b = QPushButton(label)
            b.setObjectName(obj)
            b.setFixedHeight(28)
            b.clicked.connect(fn)
            io_row.addWidget(b)
        cl.addLayout(io_row)

        parent.addWidget(card)
        self._refresh_profile_list()

    def _build_links_card(self, parent: QVBoxLayout) -> None:
        card = self._card()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(12, 10, 12, 10)
        cl.setSpacing(7)

        row = QHBoxLayout()
        row.setSpacing(6)

        discord_btn = QPushButton("Discord")
        discord_btn.setObjectName("btnDiscord")
        discord_btn.setFixedHeight(28)
        discord_btn.clicked.connect(
            lambda: __import__("webbrowser").open("https://discord.gg/2fraBuhe3m"))
        row.addWidget(discord_btn)

        reset_btn = QPushButton("Reset Settings")
        reset_btn.setObjectName("btnDanger")
        reset_btn.setFixedHeight(28)
        reset_btn.clicked.connect(self._reset_settings)
        row.addWidget(reset_btn)

        cl.addLayout(row)
        parent.addWidget(card)

    def _reset_settings(self) -> None:
        from ..utils.constants import DEFAULT_SETTINGS
        self._s = deepcopy(DEFAULT_SETTINGS)
        self._sync_all_widgets()
        self._push()

    def _prof_save(self) -> None:
        name = self._prof_name.text().strip()
        if not name:
            return
        self._profiles[name] = deepcopy(self._s)
        self._auto_save()
        self._refresh_profile_list()

    def _prof_load(self) -> None:
        name = self._prof_name.text().strip()
        if name not in self._profiles:
            return
        loaded = deepcopy(self._profiles[name])
        loaded["visible"] = self._s.get("visible", True)
        self._s = loaded
        self._sync_all_widgets()
        self._push()

    def _prof_del(self) -> None:
        name = self._prof_name.text().strip()
        if name in self._profiles:
            del self._profiles[name]
            self._auto_save()
            self._refresh_profile_list()

    def _prof_export(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Export crosshair profile", "", "JSON files (*.json)")
        if path:
            export_profile(self._s, path)

    def _prof_import(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Import crosshair profile", "", "JSON files (*.json)")
        if not path:
            return
        data = import_profile(path)
        if data is None:
            return
        name = os.path.splitext(os.path.basename(path))[0]
        base, n = name, 1
        while name in self._profiles:
            name = f"{base} ({n})"
            n += 1
        self._profiles[name] = data
        self._auto_save()
        self._refresh_profile_list()
        self._prof_name.setText(name)

    def _refresh_profile_list(self) -> None:
        self._profile_list.clear()
        for name in self._profiles:
            self._profile_list.addItem(name)

    def _on_key_captured(self, setting_key: str, key: str, source: "KeyCaptureButton") -> None:
        for sk, btn in [("toggle_hotkey", self._btn_toggle_key), ("zoom_hotkey", self._btn_zoom_key)]:
            if btn is not source and btn.current_key() == key:
                btn.set_key("")
                self._set(sk, "")
        self._set(setting_key, key)

    def _set(self, key: str, value) -> None:
        self._s[key] = value
        self._push()

    def _on_vis_toggle(self, v: bool) -> None:
        self._set("visible", v)
        if hasattr(self, "_title_bar"):
            self._title_bar.set_eye(v)
        self._sw_vis.blockSignals(True)
        self._sw_vis.setChecked(v, animate=False)
        self._sw_vis.blockSignals(False)

    def _quit(self) -> None:
        self._hotkeys.stop()
        self._zoom.stop_zoom()
        import os
        os._exit(0)

    def _push(self) -> None:
        self._overlay.apply_settings(self._s)
        self._zoom.apply_settings(self._s)
        self._hotkeys.configure(self._s)
        self._hotkeys.restart()
        if hasattr(self, "_preview"):
            self._preview.update_settings(self._s)
        self._auto_save()

    def _auto_save(self) -> None:
        save_settings(self._s, self._profiles)

    def _sync_all_widgets(self) -> None:
        s = self._s

        self._preview.update_settings(s)

        self._sw_dot.blockSignals(True);     self._sw_dot.setChecked(s.get("dot_enabled", False), animate=False);     self._sw_dot.blockSignals(False)
        self._sp_dot.blockSignals(True);     self._sp_dot.setValue(s.get("dot_size", 3));      self._sp_dot.blockSignals(False)
        self._sp_len.blockSignals(True);     self._sp_len.setValue(s.get("length",    8));      self._sp_len.blockSignals(False)
        self._sp_thick.blockSignals(True);   self._sp_thick.setValue(s.get("thickness",2));     self._sp_thick.blockSignals(False)
        self._sp_gap.blockSignals(True);     self._sp_gap.setValue(s.get("gap",        4));     self._sp_gap.blockSignals(False)

        self._sw_outline.blockSignals(True); self._sw_outline.setChecked(s.get("outline_enabled", False), animate=False); self._sw_outline.blockSignals(False)
        self._sp_out_thick.blockSignals(True);self._sp_out_thick.setValue(s.get("outline_thickness",1));self._sp_out_thick.blockSignals(False)

        if self._color_target == "outline":
            self._apply_outline_color(s.get("outline_color", "#000000"), from_target=True)
        else:
            self._apply_color(s.get("color", "#00FF00"))
        self._sp_opacity.blockSignals(True);self._sp_opacity.setValue(s.get("opacity",220));self._sp_opacity.blockSignals(False)

        self._sw_vis.blockSignals(True);     self._sw_vis.setChecked(s.get("visible", True), animate=False);          self._sw_vis.blockSignals(False)
        self._title_bar.set_eye(s.get("visible", True))
        self._btn_toggle_key.set_key(s.get("toggle_hotkey", ""))
        self._sw_rc.blockSignals(True);      self._sw_rc.setChecked(s.get("right_click_hide", True), animate=False);  self._sw_rc.blockSignals(False)
        self._dd_rc_mode.set_value(s.get("right_click_mode", "hold"))

        self._sw_zoom.blockSignals(True);    self._sw_zoom.setChecked(s.get("zoom_enabled", True), animate=False);    self._sw_zoom.blockSignals(False)
        self._btn_zoom_key.set_key(s.get("zoom_hotkey", "c"))
        self._dd_zoom_mode.set_value(s.get("zoom_mode", "hold"))
        self._sp_factor.blockSignals(True); self._sp_factor.setValue(s.get("zoom_factor",3.0)); self._sp_factor.blockSignals(False)
        self._sp_zoom_sz.blockSignals(True);self._sp_zoom_sz.setValue(s.get("zoom_size",300));  self._sp_zoom_sz.blockSignals(False)
        self._dd_anchor.set_value(s.get("zoom_anchor", "below"))
        self._sp_zoom_x.blockSignals(True); self._sp_zoom_x.setValue(s.get("zoom_x",0));         self._sp_zoom_x.blockSignals(False)
        self._sp_zoom_y.blockSignals(True); self._sp_zoom_y.setValue(s.get("zoom_y",0));         self._sp_zoom_y.blockSignals(False)
        self._custom_xy.setVisible(s.get("zoom_anchor","below") == "set")

    def _on_pin(self, pinned: bool) -> None:
        import sys
        if sys.platform == "win32":
            import ctypes
            import ctypes.wintypes
            hwnd = ctypes.wintypes.HWND(int(self.winId()))
            HWND_TOPMOST   = ctypes.wintypes.HWND(-1)
            HWND_NOTOPMOST = ctypes.wintypes.HWND(-2)
            SWP_NOMOVE     = 0x0002
            SWP_NOSIZE     = 0x0001
            SWP_NOACTIVATE = 0x0010
            ctypes.windll.user32.SetWindowPos(
                hwnd,
                HWND_TOPMOST if pinned else HWND_NOTOPMOST,
                0, 0, 0, 0,
                SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE,
            )
        else:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, pinned)
            self.show()

    def closeEvent(self, e) -> None:
        e.ignore()
        self.hide()
