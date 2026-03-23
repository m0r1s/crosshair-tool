# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ["src/crosshair/main.py"],
    pathex=["src"],
    binaries=[],
    datas=[
        ("src/crosshair/ui/arrow_up.svg", "."),
        ("src/crosshair/ui/arrow_down.svg", "."),
    ],
    hiddenimports=[
        "pynput.keyboard._win32",
        "pynput.mouse._win32",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name="crosshair",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="icon.ico",
    disable_windowed_traceback=False,
    onefile=True,
)
