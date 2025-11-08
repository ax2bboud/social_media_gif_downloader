from PyInstaller.utils.hooks import copy_metadata

# Add the imageio and imageio-ffmpeg metadata to the bundle
datas = copy_metadata('imageio')
datas += copy_metadata('imageio-ffmpeg')