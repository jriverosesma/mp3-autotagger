# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

added_files = [
    ('mp3_autotagger/assets', 'assets'),
    ('mp3_autotagger/translations', 'translations')
]

# Determine icon based on OS
if os.name == 'nt':  # Windows
    icon_path = 'mp3_autotagger/assets/main_icon.ico'
elif os.sys.platform == 'darwin':  # macOS
    icon_path = 'mp3_autotagger/assets/main_icon.icns'
elif os.sys.platform == 'linux':  # Linux
    icon_path = 'mp3_autotagger/assets/main_icon.png'
else:
    icon_path = None  # Fallback, no icon

a = Analysis(
    ['mp3_autotagger/__main__.py'],
    pathex=['mp3_autotagger'],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
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
    [],
    name='mp3_autotagger',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)
