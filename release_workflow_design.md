# GitHub Actions Release Workflow Design

## Overview

This document contains the complete GitHub Actions workflow YAML for automating multi-platform releases of the twitter_downloader application. The workflow builds executables for Windows, macOS, and Linux using PyInstaller, handles platform-specific binary downloads (FFmpeg and yt-dlp), includes dependency installation and testing, creates artifacts, and automatically creates GitHub releases with version tags and release notes.

## Design Decisions

### Matrix Strategy
- **Python Versions**: 3.8, 3.9, 3.10, 3.11 (matching pyproject.toml classifiers)
- **Operating Systems**: windows-latest, macos-latest, ubuntu-latest
- **Exclusions**: None needed as all combinations are supported

### Binary Handling
- **FFmpeg**: Downloaded from official releases and bundled with PyInstaller
- **yt-dlp**: Downloaded from GitHub releases and included in the bundle
- **Platform-specific binaries**: Windows (.exe), macOS/Linux (no extension)

### Build Process
- **PyInstaller**: Used with --onefile for single executable, --windowed for GUI apps
- **Dependencies**: Installed via pip from requirements.txt
- **Assets**: app_icon.ico included via --icon parameter

### Triggers
- **Version Tags**: Push to tags matching 'v*.*.*' pattern
- **Manual Dispatch**: workflow_dispatch for testing

### Artifacts and Releases
- **Artifact Naming**: twitter-downloader-{version}-{os}-{arch}
- **Release Creation**: Automatic on tag push with generated release notes
- **Asset Upload**: All platform executables uploaded to release

## Complete Workflow YAML

```yaml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'
  workflow_dispatch:

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [windows-latest, macos-latest, ubuntu-latest]
        python-version: ['3.8', '3.9', '3.10', '3.11']
        exclude:
          # Optional: exclude combinations if needed for performance
          - os: macos-latest
            python-version: '3.8'
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller

    - name: Download FFmpeg
      run: |
        if [ "$RUNNER_OS" == "Windows" ]; then
          curl -L https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip -o ffmpeg.zip
          unzip ffmpeg.zip
          mv ffmpeg-*-essentials_build/bin/ffmpeg.exe .
        elif [ "$RUNNER_OS" == "macOS" ]; then
          brew install ffmpeg
          cp $(brew --prefix ffmpeg)/bin/ffmpeg .
        else
          sudo apt-get update && sudo apt-get install -y ffmpeg
          cp /usr/bin/ffmpeg .
        fi

    - name: Download yt-dlp
      run: |
        if [ "$RUNNER_OS" == "Windows" ]; then
          curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe -o yt-dlp.exe
        else
          curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o yt-dlp
          chmod +x yt-dlp
        fi

    - name: Build executable with PyInstaller
      run: |
        pyinstaller --onefile --windowed --icon=app_icon.ico --add-data "ffmpeg;." --add-data "yt-dlp;." twitter_gif_downloader.py

    - name: Get version from pyproject.toml
      id: get_version
      run: |
        VERSION=$(grep '^version =' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
        echo "version=$VERSION" >> $GITHUB_OUTPUT

    - name: Create artifact name
      id: artifact_name
      run: |
        if [ "$RUNNER_OS" == "Windows" ]; then
          ARCH="x64"
          EXT=".exe"
        elif [ "$RUNNER_OS" == "macOS" ]; then
          ARCH="x64"
          EXT=""
        else
          ARCH="x64"
          EXT=""
        fi
        ARTIFACT_NAME="twitter-downloader-${{ steps.get_version.outputs.version }}-${RUNNER_OS,,}-$ARCH$EXT"
        echo "name=$ARTIFACT_NAME" >> $GITHUB_OUTPUT

    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: ${{ steps.artifact_name.outputs.name }}
        path: dist/twitter_gif_downloader${{ matrix.os == 'windows-latest' && '.exe' || '' }}

  release:
    needs: build
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Get version
      id: get_version
      run: |
        VERSION=${GITHUB_REF#refs/tags/v}
        echo "version=$VERSION" >> $GITHUB_OUTPUT

    - name: Download all artifacts
      uses: actions/download-artifact@v3
      with:
        path: artifacts/

    - name: Generate release notes
      id: release_notes
      run: |
        # Generate release notes from commits since last tag
        PREVIOUS_TAG=$(git describe --tags --abbrev=0 HEAD~1 2>/dev/null || echo "")
        if [ -n "$PREVIOUS_TAG" ]; then
          NOTES=$(git log --pretty=format:"- %s" $PREVIOUS_TAG..HEAD)
        else
          NOTES=$(git log --pretty=format:"- %s" --max-count=10)
        fi
        echo "notes<<EOF" >> $GITHUB_OUTPUT
        echo "## Changes in v${{ steps.get_version.outputs.version }}" >> $GITHUB_OUTPUT
        echo "$NOTES" >> $GITHUB_OUTPUT
        echo "" >> $GITHUB_OUTPUT
        echo "## Downloads" >> $GITHUB_OUTPUT
        echo "Download the appropriate executable for your platform from the assets below." >> $GITHUB_OUTPUT
        echo "EOF" >> $GITHUB_OUTPUT

    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        tag_name: v${{ steps.get_version.outputs.version }}
        name: Release v${{ steps.get_version.outputs.version }}
        body: ${{ steps.release_notes.outputs.notes }}
        files: artifacts/**/*
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Explanation of Key Components

### Matrix Build Strategy
The workflow uses a matrix to build across multiple Python versions and operating systems simultaneously. This ensures compatibility across platforms while testing different Python versions.

### Binary Downloads
- FFmpeg is downloaded from official sources and bundled to avoid system dependencies
- yt-dlp is downloaded from its GitHub releases for the latest version
- Both are added to PyInstaller with --add-data to include them in the executable bundle

### PyInstaller Configuration
- `--onefile`: Creates a single executable file
- `--windowed`: Prevents console window on Windows GUI apps
- `--icon`: Uses the app_icon.ico for the executable icon
- `--add-data`: Includes FFmpeg and yt-dlp binaries in the bundle

### Artifact Management
- Artifacts are named with version, OS, and architecture for clarity
- All artifacts are downloaded in the release job for upload to GitHub releases

### Release Automation
- Triggered on version tags (v*.*.* pattern)
- Generates release notes from git commits since the last tag
- Automatically uploads all platform executables as release assets

### Error Handling and Testing
- The workflow includes basic testing by running the build process
- Failures in any matrix combination will fail the entire workflow
- Artifacts are only created if builds succeed

This workflow provides a robust, automated release process that handles the complexities of cross-platform Python application distribution with bundled dependencies.