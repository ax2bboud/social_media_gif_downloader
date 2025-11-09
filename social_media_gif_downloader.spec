# -*- mode: python ; coding: utf-8 -*-

import sys
import os
import platform
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

block_cipher = None

# Collect all necessary data files and hidden imports
datas = []
datas += collect_data_files('customtkinter')
datas += collect_data_files('yt_dlp')
datas += collect_data_files('imageio')
datas += collect_data_files('pycryptodomex')


# Collect binaries (including dynamic libraries)
binaries = []
binaries += collect_dynamic_libs('customtkinter')

# Add ffmpeg binary if available
ffmpeg_binary = None
if os.path.exists('ffmpeg.exe') or os.path.exists('ffmpeg'):
    ffmpeg_name = 'ffmpeg.exe' if platform.system() == 'Windows' else 'ffmpeg'
    if os.path.exists(ffmpeg_name):
        binaries.append((ffmpeg_name, '.'))
        print(f"[INFO] Found and bundling ffmpeg: {ffmpeg_name}")
    else:
        print(f"[WARNING] ffmpeg binary not found at {ffmpeg_name}")
else:
    # Try to find ffmpeg from imageio-ffmpeg package (bundled with moviepy)
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        if ffmpeg_path and os.path.exists(ffmpeg_path):
            ffmpeg_name = 'ffmpeg.exe' if platform.system() == 'Windows' else 'ffmpeg'
            binaries.append((ffmpeg_path, '.'))
            print(f"[INFO] Found and bundling ffmpeg from imageio-ffmpeg: {ffmpeg_path}")
        else:
            print("[WARNING] imageio-ffmpeg ffmpeg not found")
    except ImportError:
        print("[WARNING] imageio-ffmpeg not installed, ffmpeg may not be bundled")

# Add yt-dlp binary if available (for platforms where yt-dlp is bundled as binary)
yt_dlp_name = 'yt-dlp.exe' if platform.system() == 'Windows' else 'yt-dlp'
if os.path.exists(yt_dlp_name):
    binaries.append((yt_dlp_name, '.'))
    print(f"[INFO] Found and bundling yt-dlp binary: {yt_dlp_name}")

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
    'pycryptodomex',
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
