# Building Platform-Specific Executables

This document explains how to build platform-specific executables for the Social Media GIF Downloader application with all required dependencies bundled.

## Key Dependencies Bundled

Each executable includes:
- **Python runtime** - Complete Python interpreter
- **FFmpeg** - Video processing binary (platform-specific)
- **yt-dlp** - Social media downloader (as Python module)
- **CustomTkinter** - GUI library with all data files
- **MoviePy** - Video processing with imageio-ffmpeg
- **All Python dependencies** - numpy, imageio, PIL, etc.

## Automated Builds via GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/build-executables.yml`) that automatically builds executables for all platforms when you push a version tag.

### Triggering a Release Build

1. Ensure your version is updated in:
   - `pyproject.toml`
   - `social_media_gif_downloader.py` (`__version__` variable)
   - `__init__.py`

2. Create and push a version tag:
   ```bash
   git tag v1.0.5
   git push origin v1.0.5
   ```

3. The workflow will automatically:
   - Download and bundle platform-specific FFmpeg binaries
   - Build Windows `.exe` with embedded FFmpeg
   - Build macOS `.app` (packaged as `.dmg`) with embedded FFmpeg
   - Build Linux `.AppImage` with embedded FFmpeg
   - Verify all executables are properly built
   - Create a GitHub release with all binaries attached

### Manual Workflow Trigger

You can also manually trigger the build workflow from the GitHub Actions tab without creating a tag. This is useful for testing builds before release.

## Platform-Specific Details

### Windows (.exe)

**Requirements:**
- Windows runner (GitHub Actions provides `windows-latest`)
- Python 3.12
- PyInstaller
- imageio-ffmpeg

**FFmpeg Source:** https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip

**Output:** `SocialMediaGIFDownloader-Windows-x64.zip` containing the `.exe` file

**Features:**
- Single executable file (~150-200 MB)
- Windowed application (no console window)
- Embedded icon from `app_icon.ico`
- FFmpeg binary bundled directly into executable
- All dependencies bundled (no external requirements)

**Build Process:**
1. Downloads FFmpeg essentials build
2. Extracts and copies `ffmpeg.exe` to build directory
3. PyInstaller bundles it into the executable using spec file
4. Application detects frozen mode and uses bundled FFmpeg

### macOS (.app / .dmg)

**Requirements:**
- macOS runner (GitHub Actions provides `macos-latest`)
- Python 3.12
- PyInstaller
- imageio-ffmpeg
- `create-dmg` tool for packaging

**FFmpeg Source:** https://evermeet.cx/ffmpeg/getrelease/ffmpeg/zip

**Output:** `SocialMediaGIFDownloader-macOS.dmg` (or `.zip` as fallback)

**Features:**
- macOS application bundle (.app)
- Packaged as a disk image (.dmg) for easy installation
- Drag-to-Applications support
- High DPI (Retina) support enabled
- Dark mode compatible
- FFmpeg binary bundled in app bundle

**Build Process:**
1. Downloads FFmpeg binary for macOS
2. Extracts and copies `ffmpeg` to build directory
3. PyInstaller bundles it into the .app bundle
4. create-dmg packages the .app into a .dmg installer

### Linux (AppImage)

**Requirements:**
- Ubuntu runner (GitHub Actions provides `ubuntu-latest`)
- Python 3.12
- PyInstaller
- imageio-ffmpeg
- `appimagetool`
- FUSE support (for running AppImages)
- python3-tk (for tkinter support)

**FFmpeg Source:** https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz

**Output:** `SocialMediaGIFDownloader-Linux-x86_64.AppImage`

**Features:**
- Self-contained executable
- No installation required
- Portable across Linux distributions
- Desktop integration via embedded `.desktop` file
- Static FFmpeg binary bundled

**Build Process:**
1. Downloads static FFmpeg build for Linux
2. Extracts and copies `ffmpeg` to build directory
3. PyInstaller creates the executable with bundled FFmpeg
4. AppImage structure is created with proper desktop integration
5. appimagetool packages everything into .AppImage

## Local Development Builds

### Prerequisites

Install build dependencies:
```bash
pip install pyinstaller imageio-ffmpeg
```

### Download FFmpeg for Local Builds

**Windows (PowerShell):**
```powershell
# Download FFmpeg
Invoke-WebRequest -Uri "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -OutFile "ffmpeg.zip"
Expand-Archive -Path "ffmpeg.zip" -DestinationPath "ffmpeg_temp"
# Find and copy ffmpeg.exe to project root
Get-ChildItem -Path ffmpeg_temp -Filter ffmpeg.exe -Recurse | Select-Object -First 1 | Copy-Item -Destination "ffmpeg.exe"
Remove-Item -Recurse -Force ffmpeg_temp
Remove-Item ffmpeg.zip
```

**macOS:**
```bash
curl -L https://evermeet.cx/ffmpeg/getrelease/ffmpeg/zip -o ffmpeg.zip
unzip ffmpeg.zip
rm ffmpeg.zip
chmod +x ffmpeg
```

**Linux:**
```bash
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar -xf ffmpeg-release-amd64-static.tar.xz
find . -name ffmpeg -type f -executable -exec cp {} ffmpeg \;
rm -rf ffmpeg-release-amd64-static*
chmod +x ffmpeg
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

### Test the Build

Before distributing, test the executable:

```bash
# Create a test script
python test_build.py
```

Then run the actual executable to verify:
- GUI launches without errors
- Download functionality works
- GIF conversion works (requires FFmpeg)
- All UI elements render correctly

### Clean Build

To perform a clean build (removes cached files):

```bash
pyinstaller social_media_gif_downloader.spec --clean
```

## PyInstaller Spec File Configuration

The `social_media_gif_downloader.spec` file configures PyInstaller bundling:

### Key Features:

1. **Data Files Collection:**
   - CustomTkinter themes and assets
   - yt-dlp data files

2. **Binary Collection:**
   - FFmpeg executable (platform-specific)
   - CustomTkinter dynamic libraries
   - Optional yt-dlp binary

3. **Hidden Imports:**
   - All CustomTkinter submodules
   - All yt-dlp submodules
   - All MoviePy submodules
   - imageio-ffmpeg
   - tkinter and _tkinter
   - Various yt-dlp dependencies (websockets, brotli, pycryptodomex, etc.)

4. **Exclusions:**
   - Large unused packages (matplotlib, scipy, pandas, IPython)
   - Reduces executable size

5. **Platform-Specific Settings:**
   - Windows: No console window, embedded icon
   - macOS: App bundle with Info.plist configuration
   - Linux: Standard executable

## Runtime FFmpeg Detection

The application uses a multi-layer approach to find FFmpeg:

1. **Bundled FFmpeg (frozen mode):**
   - Checks `sys._MEIPASS` directory for platform-specific FFmpeg binary
   - Sets `FFMPEG_BINARY` and `IMAGEIO_FFMPEG_EXE` environment variables
   - This is the primary method for distributed executables

2. **imageio-ffmpeg Fallback:**
   - If bundled FFmpeg not found, tries imageio-ffmpeg package
   - Provides cross-platform FFmpeg support in development

3. **System FFmpeg:**
   - MoviePy can use system-installed FFmpeg as last resort
   - Not reliable for end users

## Troubleshooting

### Build Issues

**FFmpeg Not Bundled:**
- Verify ffmpeg binary exists in project root before running PyInstaller
- Check PyInstaller output for FFmpeg bundling messages
- Look for "[INFO] Found and bundling ffmpeg" in build output

**Missing Python Modules:**
1. Add the module to `hiddenimports` in the spec file
2. If it's a package with data files, add it to `datas` using `collect_data_files`

**tkinter Errors:**
- Ensure tkinter is installed on the build system
- Linux: Install `python3-tk` package
- Add `_tkinter` and `tkinter` to `hiddenimports`

### Runtime Issues

**FFmpeg Not Found (in bundled executable):**
- Check the log file created by the executable
- Verify FFmpeg was bundled (check executable size - should be 150-200 MB)
- Look for "FFmpeg not found in bundle" warnings in logs

**Video Download Works but GIF Conversion Fails:**
- FFmpeg bundling issue
- Check log file for FFmpeg path errors
- Verify moviepy can locate FFmpeg

**GUI Doesn't Launch:**
- tkinter or CustomTkinter not properly bundled
- Check for missing data files
- Verify CustomTkinter themes were collected

### Large Executable Size

Expected sizes:
- Windows: ~150-200 MB
- macOS: ~180-220 MB
- Linux: ~160-210 MB

Includes:
- Python runtime (~50 MB)
- FFmpeg binary (~50-80 MB depending on platform)
- All dependencies (moviepy, CustomTkinter, yt-dlp, numpy, imageio, etc.)

This is normal for self-contained Python executables with video processing.

### Platform-Specific Issues

**Windows:**
- Antivirus may flag PyInstaller executables (false positive)
- Users may need to add security exception
- Windows SmartScreen may show warning on first run

**macOS:**
- Users may see "unidentified developer" warning
- Solution: Right-click → Open (first time only)
- For distribution: Sign and notarize the app (requires Apple Developer account)

**Linux:**
- Users need FUSE to run AppImages: `sudo apt install fuse libfuse2`
- Make AppImage executable: `chmod +x SocialMediaGIFDownloader-*.AppImage`
- Some distributions require additional desktop integration

## Verifying Builds

### Automated Verification

The GitHub Actions workflow includes verification steps:
1. Checks that executable/app files exist
2. Verifies file sizes are reasonable
3. Lists bundled files

### Manual Testing Checklist

For each platform:
- [ ] Executable launches without errors
- [ ] GUI renders correctly
- [ ] Can download Twitter video
- [ ] Can download Pinterest video
- [ ] Can convert video to GIF
- [ ] Can download video (MP4) without conversion
- [ ] Settings persist between sessions
- [ ] File dialog works for choosing save location
- [ ] No Python installation required on test machine
- [ ] No FFmpeg installation required

## Release Checklist

Before creating a release:

1. ✅ Update version in all files (pyproject.toml, .py files)
2. ✅ Run tests: `pytest --cov=social_media_gif_downloader --cov-report=xml --ignore=tests/test_integration.py`
3. ✅ Test local build on at least one platform
4. ✅ Verify FFmpeg is bundled in local build
5. ✅ Update CHANGELOG or release notes
6. ✅ Create and push version tag
7. ✅ Monitor GitHub Actions workflow for all three platforms
8. ✅ Download artifacts from GitHub Actions
9. ✅ Test each platform executable:
   - Windows: Test on clean Windows VM
   - macOS: Test on clean macOS machine
   - Linux: Test on Ubuntu/Fedora
10. ✅ Verify all executables work without external dependencies
11. ✅ Update README with latest release link

## Continuous Integration

The build workflow integrates with existing CI:

- **CI Tests** (`.github/workflows/ci.yml`): Runs on every push/PR
- **Release** (`.github/workflows/release.yml`): Builds Python packages and publishes to PyPI
- **Build Executables** (`.github/workflows/build-executables.yml`): Builds platform binaries with bundled FFmpeg

All workflows are triggered by version tags for comprehensive releases.

## Security Considerations

### Binary Verification
- All FFmpeg binaries are downloaded from official sources
- URLs are hardcoded in the workflow (no user input)
- GitHub Actions provides build provenance

### Code Signing
Currently, binaries are not code-signed. For production:
- **Windows:** Use SignTool with a code signing certificate
- **macOS:** Use codesign and notarize with Apple Developer account
- **Linux:** AppImages support signing (optional)

### Antivirus False Positives
PyInstaller executables may trigger antivirus warnings:
- This is common for PyInstaller apps
- Can be mitigated with code signing
- Users may need to add exceptions

## Support and Debugging

If users report issues with executables:

1. Ask for the log file:
   - Windows: Same directory as .exe
   - macOS: Inside .app bundle
   - Linux: Same directory as AppImage

2. Check for common issues:
   - FFmpeg path errors
   - Module import errors
   - tkinter/GUI errors

3. Verify their environment:
   - OS version
   - Available disk space
   - Internet connectivity
   - Antivirus/firewall settings
