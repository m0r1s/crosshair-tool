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

"""QSS stylesheet – mirrors moris macro maker theme exactly."""

import os
import sys

from ..utils.constants import FONT

def _res(filename: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(base, filename).replace("\\", "/")

_ARROW_UP   = _res("arrow_up.svg")
_ARROW_DOWN = _res("arrow_down.svg")

SS: str = f"""
QWidget {{
    background: transparent;
    color: #f0f0f0;
    font-family: {FONT};
    font-size: 12px;
}}
QWidget#mainContainer {{
    background: #121212;
    border-radius: 12px;
}}
QWidget#titleBar {{
    background: #0a0a0a;
    border-top-left-radius:  12px;
    border-top-right-radius: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}}
QFrame#sep  {{ background: rgba(255,255,255,0.07); border: none; }}
QFrame#divV {{ background: rgba(255,255,255,0.07); border: none; }}

QPushButton:focus {{ outline: none; }}

QPushButton#btnClose {{
    background: transparent; border: none;
    color: #52596b; font-size: 11px; font-weight: 700;
    border-radius: 5px;
    font-family: {FONT};
}}
QPushButton#btnClose:hover {{ background: rgba(255,90,112,0.18); color: #ff5a70; }}
QPushButton#btnMinimize {{
    background: transparent; border: none;
    border-radius: 5px;
}}
QPushButton#btnMinimize:hover {{ background: rgba(255,220,50,0.18); }}

QPushButton#btnPin {{
    background: transparent; border: none;
    color: #52596b; font-size: 11px; font-weight: 600;
    border-radius: 5px;
}}
QPushButton#btnPin:hover {{ background: rgba(255,255,255,0.07); color: #c0c0c0; }}
QPushButton#btnPinOn {{
    background: rgba(137,223,255,0.13); border: none;
    color: #89dfff; font-size: 11px; font-weight: 600;
    border-radius: 5px;
}}
QPushButton#btnPinOn:hover {{ background: rgba(137,223,255,0.22); }}

/* ---------- settings cards (matches macro_maker) ---------- */
QWidget#settingsCard {{
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
}}
QWidget#previewCard {{
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
}}

/* ---------- buttons ---------- */
QPushButton#btnPrimary {{
    background: rgba(137,223,255,0.11);
    border: 1px solid rgba(137,223,255,0.26);
    color: #89dfff;
    font-size: 11px; font-weight: 600;
    border-radius: 8px;
    font-family: {FONT};
}}
QPushButton#btnPrimary:hover   {{ background: rgba(137,223,255,0.20); border-color: rgba(137,223,255,0.50); }}
QPushButton#btnPrimary:pressed {{ background: rgba(137,223,255,0.28); }}
QPushButton#btnPrimary:disabled {{
    background: rgba(137,223,255,0.03); border-color: rgba(137,223,255,0.08);
    color: rgba(137,223,255,0.22);
}}

QPushButton#btnDiscord {{
    background: rgba(88,101,242,0.20);
    border: 1px solid rgba(88,101,242,0.45);
    color: #8891f2;
    font-size: 11px; font-weight: 600;
    border-radius: 8px;
    font-family: {FONT};
}}
QPushButton#btnDiscord:hover   {{ background: rgba(88,101,242,0.35); border-color: rgba(88,101,242,0.70); color: #c0c6ff; }}
QPushButton#btnDiscord:pressed {{ background: rgba(88,101,242,0.50); }}

QPushButton#btnDanger {{
    background: rgba(255,75,105,0.10);
    border: 1px solid rgba(255,75,105,0.30);
    color: #ff4b69;
    font-size: 11px; font-weight: 600;
    border-radius: 8px;
    font-family: {FONT};
}}
QPushButton#btnDanger:hover   {{ background: rgba(255,75,105,0.20); border-color: rgba(255,75,105,0.52); }}
QPushButton#btnDanger:pressed {{ background: rgba(255,75,105,0.30); }}

QPushButton#btnNeutral {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    color: #aaaaaa;
    font-size: 11px; font-weight: 600;
    border-radius: 8px;
    font-family: {FONT};
}}
QPushButton#btnNeutral:hover   {{ background: rgba(255,255,255,0.10); color: #d8d8d8; }}
QPushButton#btnNeutral:pressed {{ background: rgba(255,255,255,0.16); }}
QPushButton#btnNeutral:disabled {{ color: #333; border-color: rgba(255,255,255,0.05); }}

/* ---------- key capture button ---------- */
QPushButton#btnKey {{
    background: #0e0e0e;
    border: 1px solid rgba(255,255,255,0.10);
    color: #f0f0f0;
    font-size: 11px; font-weight: 600;
    border-radius: 6px;
    font-family: {FONT};
}}
QPushButton#btnKey:hover {{ border-color: rgba(137,223,255,0.50); }}

/* ---------- line-visibility toggle buttons ---------- */
QPushButton#lineBtn {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    color: #52596b;
    font-size: 10px; font-weight: 700;
    border-radius: 5px;
    font-family: {FONT};
}}
QPushButton#lineBtn:hover {{ background: rgba(255,255,255,0.09); color: #aaaaaa; }}
QPushButton#lineBtnOn {{
    background: rgba(137,223,255,0.15);
    border: 1px solid rgba(137,223,255,0.40);
    color: #89dfff;
    font-size: 10px; font-weight: 700;
    border-radius: 5px;
    font-family: {FONT};
}}
QPushButton#lineBtnOn:hover {{ background: rgba(137,223,255,0.22); }}

/* ---------- type dropdown (same as macro_maker) ---------- */
QPushButton#btnTypeDropdown {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    color: #7a8299;
    font-size: 11px; font-weight: 600;
    border-radius: 6px;
    padding: 0px 10px;
    text-align: left;
    font-family: {FONT};
}}
QPushButton#btnTypeDropdown:hover {{
    background: rgba(255,255,255,0.09);
    border-color: rgba(255,255,255,0.18);
    color: #eef0f5;
}}
QFrame#typePopupInner {{
    background: #1a1a1a;
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 8px;
}}
QPushButton#btnTypeOption {{
    background: transparent; border: none;
    color: #c0c5d0; font-size: 11px; font-weight: 500;
    border-radius: 5px; padding: 0px 8px; text-align: left;
    font-family: {FONT};
}}
QPushButton#btnTypeOption:hover {{ background: rgba(137,223,255,0.10); color: #89dfff; }}
QPushButton#btnTypeOptionSel {{
    background: rgba(137,223,255,0.12); border: none;
    color: #89dfff; font-size: 11px; font-weight: 600;
    border-radius: 5px; padding: 0px 8px; text-align: left;
    font-family: {FONT};
}}
QPushButton#btnTypeOptionSel:hover {{ background: rgba(137,223,255,0.18); }}

/* ---------- spin boxes ---------- */
QSpinBox, QDoubleSpinBox {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    color: #f0f0f0;
    font-family: {FONT}; font-size: 12px;
    padding: 0 6px; border-radius: 6px; height: 26px;
}}
QSpinBox:focus, QDoubleSpinBox:focus {{ border-color: #89dfff; }}
QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-origin: border; subcontrol-position: top right;
    width: 16px; border-left: 1px solid rgba(255,255,255,0.08);
    border-top-right-radius: 6px; background: rgba(255,255,255,0.04);
}}
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border; subcontrol-position: bottom right;
    width: 16px; border-left: 1px solid rgba(255,255,255,0.08);
    border-bottom-right-radius: 6px; background: rgba(255,255,255,0.04);
}}
QSpinBox::up-button:hover,   QDoubleSpinBox::up-button:hover   {{ background: rgba(255,255,255,0.09); }}
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{ background: rgba(255,255,255,0.09); }}
QSpinBox::up-arrow,   QDoubleSpinBox::up-arrow   {{ image: url({_ARROW_UP}); width: 6px; height: 4px; }}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{ image: url({_ARROW_DOWN}); width: 6px; height: 4px; }}

/* ---------- line edit / key input ---------- */
QLineEdit#keyInput {{
    background: #080808;
    border: 1px solid rgba(255,255,255,0.10);
    color: #f0f0f0;
    font-family: {FONT}; font-size: 12px; font-weight: 600;
    padding: 0 5px; border-radius: 6px; height: 26px;
}}
QLineEdit#keyInput:focus {{ border-color: #89dfff; background: #0e0e0e; }}
QLineEdit {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    color: #f0f0f0; font-family: {FONT}; font-size: 12px;
    padding: 0 7px; border-radius: 6px; height: 26px;
}}
QLineEdit:focus {{ border-color: #89dfff; background: #0e0e0e; }}

/* ---------- list widget ---------- */
QListWidget {{
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 6px;
    color: #f0f0f0; font-family: {FONT}; font-size: 11px;
    outline: none;
}}
QListWidget::item {{ padding: 4px 8px; border-radius: 4px; }}
QListWidget::item:selected {{ background: rgba(137,223,255,0.12); color: #89dfff; }}
QListWidget::item:hover:!selected {{ background: rgba(255,255,255,0.05); }}

/* ---------- scroll area ---------- */
QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{
    background: transparent; width: 8px; margin: 0 3px 0 0;
}}
QScrollBar::handle:vertical {{
    background: rgba(255,255,255,0.10); border-radius: 2px; min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{ background: rgba(255,255,255,0.20); }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

/* ---------- status bar ---------- */
QWidget#statusBar {{
    background: #0a0a0a;
    border-top: 1px solid rgba(255,255,255,0.07);
    border-bottom-left-radius:  12px;
    border-bottom-right-radius: 12px;
}}
"""
