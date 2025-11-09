# Building Platform-Specific Executables

This document explains how to build platform-specific executables for the Social Media GIF Downloader application.

## Automated Builds via GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/build-executables.yml`) that automatically builds executables for all platforms when you push a version tag.

### Triggering a Release Build

1. Ensure your version is updated in:
   - `pyproject.toml`
   - `social_media_gif_downloader.py` (`__version__` variable)
   - `__init__.py`

2. Create and push a version tag:
   ```bash
   git tag v1.0.4
   git push origin v1.0.4
   ```

3. The workflow will automatically:
   - Build Windows `.exe`
   - Build macOS `.app` (packaged as `.dmg`)
   - Build Linux `.AppImage`
   - Create a GitHub release with all binaries attached

### Manual Workflow Trigger

You can also manually trigger the build workflow from the GitHub Actions tab without creating a tag. This is useful for testing builds before release.

## Platform-Specific Details

### Windows (.exe)

**Requirements:**
- Windows runner (GitHub Actions provides `windows-latest`)
- Python 3.12
- PyInstaller

**Output:** `SocialMediaGIFDownloader-Windows-x64.zip` containing the `.exe` file

**Features:**
- Single executable file
- Windowed application (no console window)
- Embedded icon from `app_icon.ico`
- All dependencies bundled (including FFmpeg via moviepy)

### macOS (.app / .dmg)

**Requirements:**
- macOS runner (GitHub Actions provides `macos-latest`)
- Python 3.12
- PyInstaller
- `create-dmg` tool for packaging

**Output:** `SocialMediaGIFDownloader-macOS.dmg` (or `.zip` as fallback)

**Features:**
- macOS application bundle (.app)
- Packaged as a disk image (.dmg) for easy installation
- Drag-to-Applications support
- High DPI support enabled
- Dark mode compatible

### Linux (AppImage)

**Requirements:**
- Ubuntu runner (GitHub Actions provides `ubuntu-latest`)
- Python 3.12
- PyInstaller
- `appimagetool`
- FUSE support (for running AppImages)

**Output:** `SocialMediaGIFDownloader-Linux-x86_64.AppImage`

**Features:**
- Self-contained executable
- No installation required
- Portable across Linux distributions
- Desktop integration via embedded `.desktop` file

## Local Development Builds

### Prerequisites

Install PyInstaller:
```bash
pip install pyinstaller
```

### Build Locally

From the project root:

```bash
pyinstaller social_media_gif_downloader.spec
```

The executable will be created in the `dist/` directory:
- **Windows:** `dist/SocialMediaGIFDownloader.exe`
- **macOS:** `dist/SocialMediaGIFDownloader.app`
- **Linux:** `dist/SocialMediaGIFDownloader`

### Clean Build

To perform a clean build (removes cached files):

```bash
pyinstaller social_media_gif_downloader.spec --clean
```

## PyInstaller Spec File

The `social_media_gif_downloader.spec` file configures how PyInstaller bundles the application:

- **Data Files:** Automatically collects CustomTkinter and yt-dlp data files
- **Hidden Imports:** Ensures all necessary modules are included
- **Icon:** Uses `app_icon.ico` if available
- **Console:** Set to `False` for windowed GUI application
- **One-File Mode:** Packages everything into a single executable

## Troubleshooting

### Missing Dependencies

If the built executable fails to run due to missing modules:

1. Add the module to `hiddenimports` in the spec file
2. If it's a package with data files, add it to `datas` using `collect_data_files`

### FFmpeg Not Found

The application is designed to use FFmpeg bundled with moviepy when frozen. If FFmpeg errors occur:

1. Check that moviepy is properly installed
2. Verify the FFmpeg path detection logic in `social_media_gif_downloader.py`

### Large Executable Size

The executables include:
- Python runtime
- All dependencies (moviepy, CustomTkinter, yt-dlp)
- FFmpeg binary

This typically results in ~150-200 MB executables, which is expected.

### Platform-Specific Issues

**Windows:**
- Antivirus software may flag PyInstaller executables as suspicious (false positive)
- Users may need to add an exception or mark as safe

**macOS:**
- Users may need to allow the app in System Preferences > Security & Privacy
- For notarization, see Apple's developer documentation

**Linux:**
- Users need FUSE installed to run AppImages
- Make the AppImage executable: `chmod +x SocialMediaGIFDownloader-*.AppImage`

## Release Checklist

Before creating a release:

1. ✅ Update version in all files (pyproject.toml, .py files)
2. ✅ Run tests: `pytest --ignore=tests/test_integration.py`
3. ✅ Test build locally on at least one platform
4. ✅ Update CHANGELOG or release notes
5. ✅ Create and push version tag
6. ✅ Monitor GitHub Actions workflow
7. ✅ Test downloaded executables from release
8. ✅ Update README with latest release link

## Continuous Integration

The build workflow integrates with the existing release workflow:

- **CI Tests** (`.github/workflows/ci.yml`): Runs on every push/PR
- **Release** (`.github/workflows/release.yml`): Builds Python packages (sdist/wheel) and publishes to PyPI
- **Build Executables** (`.github/workflows/build-executables.yml`): Builds platform-specific binaries

All three workflows are triggered by version tags, ensuring comprehensive release artifacts.
