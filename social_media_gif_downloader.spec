# -*- mode: python ; coding: utf-8 -*-

import sys
# Add the project root to the Python path to allow hooks to be imported
sys.path.append(os.path.abspath("."))

import os
import platform
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs
from hooks.helpers import find_binary

block_cipher = None

# --- Collect Data Files ---
# Bundles non-code assets required by the application at runtime.
datas = []
datas += collect_data_files('customtkinter')
datas += collect_data_files('yt_dlp')
datas += collect_data_files('imageio')
datas += collect_data_files('pycryptodomex')


# --- Collect Binaries ---
# Bundles external executables and dynamic libraries.
binaries = []
binaries += collect_dynamic_libs('customtkinter')

# Add ffmpeg, ffprobe, and yt-dlp binaries using the helper
# This ensures they are found regardless of their location (root, bin, or PATH).
for binary_name in ['ffmpeg', 'ffprobe', 'yt-dlp']:
    # Add '.exe' for Windows
    if platform.system() == 'Windows':
        binary_name += '.exe'
    
    # Find the binary path using the helper
    binary_path = find_binary(binary_name)
    
    # If found, add it to the binaries list to be bundled
    if binary_path:
        binaries.append((binary_path, '.'))
        print(f"[INFO] Bundling '{binary_name}' from: {binary_path}")
    else:
        print(f"[WARNING] Could not find '{binary_name}'. It will not be bundled.")

hiddenimports = []
hiddenimports += collect_submodules('customtkinter')
hiddenimports += collect_submodules('yt_dlp')
hiddenimports += collect_submodules('moviepy')
hiddenimports += [
    'PIL._tkinter_finder',
    'imageio_ffmpeg',
    'proglog',
    'decorator',
    'imageio',
    'imageio.plugins.pillow',
    'numpy',
    'certifi',
    'charset_normalizer',
    'websockets',
    'brotli',
    'mutagen',
    'Cryptodome',
    'urllib3',
    'platforms',
    'config',
]

# Add platform-specific hidden imports
if platform.system() == 'Windows':
    hiddenimports += ['_tkinter', 'tkinter', 'tkinter.filedialog']
elif platform.system() == 'Darwin':
    hiddenimports += ['_tkinter', 'tkinter', 'tkinter.filedialog']
elif platform.system() == 'Linux':
    hiddenimports += ['_tkinter', 'tkinter', 'tkinter.filedialog']

# Add app icon
icon_file = 'app_icon.ico' if os.path.exists('app_icon.ico') else None

a = Analysis(
    ['social_media_gif_downloader.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'pandas', 'IPython'],
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
