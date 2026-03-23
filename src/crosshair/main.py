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
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

from crosshair.hotkeys import HotkeyManager
from crosshair.overlay import CrosshairOverlay
from crosshair.ui.main_window import MainWindow
from crosshair.ui.styles import SS
from crosshair.utils.constants import LOGO_B64
from crosshair.utils.settings import load_settings, save_settings
from crosshair.zoom_overlay import ZoomOverlay


def _app_icon() -> QIcon:
    padded = LOGO_B64 + "=" * (-len(LOGO_B64) % 4)
    data = base64.b64decode(padded)
    pix = QPixmap()
    pix.loadFromData(data, "ICO")
    return QIcon(pix)


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(SS)
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(_app_icon())

    settings, profiles = load_settings()

    overlay  = CrosshairOverlay(settings)
    zoom     = ZoomOverlay(settings)
    hotkeys  = HotkeyManager()

    hotkeys.configure(settings)

    _rc_toggle_state = [True]

    def on_rc_press() -> None:
        mode = overlay._settings.get("right_click_mode", "hold")
        if mode == "hold":
            overlay.set_force_hidden(True)
        else:
            _rc_toggle_state[0] = not _rc_toggle_state[0]
            overlay.set_force_hidden(not _rc_toggle_state[0])

    def on_rc_release() -> None:
        mode = overlay._settings.get("right_click_mode", "hold")
        if mode == "hold":
            overlay.set_force_hidden(False)

    def on_zoom_press() -> None:
        mode = overlay._settings.get("zoom_mode", "hold")
        if mode == "hold":
            zoom.start_zoom()
        else:
            zoom.toggle_zoom()

    def on_zoom_release() -> None:
        mode = overlay._settings.get("zoom_mode", "hold")
        if mode == "hold":
            zoom.stop_zoom()

    def on_toggle() -> None:
        cur = overlay._settings.get("visible", True)
        overlay.set_visible(not cur)
        if hasattr(win, "_sw_visible"):
            win._sw_visible.setChecked(not cur)
            win._update_status()

    hotkeys.signals.right_click_press.connect(on_rc_press)
    hotkeys.signals.right_click_release.connect(on_rc_release)
    hotkeys.signals.zoom_press.connect(on_zoom_press)
    hotkeys.signals.zoom_release.connect(on_zoom_release)
    hotkeys.signals.toggle_visibility.connect(on_toggle)

    hotkeys.start()

    win = MainWindow(overlay, zoom, hotkeys, settings, profiles)

    tray_icon = QSystemTrayIcon(_app_icon(), app)
    tray_icon.setToolTip("crosshair tool")

    tray_menu = QMenu()

    act_show = tray_menu.addAction("Show Settings")
    act_show.triggered.connect(win.show)

    act_toggle = tray_menu.addAction("Toggle Crosshair")
    def _tray_toggle() -> None:
        cur = overlay._settings.get("visible", True)
        overlay.set_visible(not cur)
        save_settings(overlay._settings, win._profiles)
    act_toggle.triggered.connect(_tray_toggle)

    tray_menu.addSeparator()

    act_quit = tray_menu.addAction("Quit")
    def _quit() -> None:
        hotkeys.stop()
        zoom.stop_zoom()
        app.quit()
    act_quit.triggered.connect(_quit)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.activated.connect(
        lambda reason: win.show()
        if reason == QSystemTrayIcon.ActivationReason.Trigger
        else None
    )
    tray_icon.show()

    overlay.show_overlay()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
