# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all necessary data files and hidden imports
datas = []
datas += collect_data_files('customtkinter')
datas += collect_data_files('yt_dlp')

hiddenimports = []
hiddenimports += collect_submodules('customtkinter')
hiddenimports += collect_submodules('yt_dlp')
hiddenimports += ['PIL._tkinter_finder']

# Add app icon
icon_file = 'app_icon.ico' if os.path.exists('app_icon.ico') else None

a = Analysis(
    ['social_media_gif_downloader.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='SocialMediaGIFDownloader',
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
    icon=icon_file,
)

# macOS app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='SocialMediaGIFDownloader.app',
        icon=icon_file,
        bundle_identifier='com.ax2bboud.socialmediagifdownloader',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'NSRequiresAquaSystemAppearance': 'False',
        },
    )
