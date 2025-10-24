#!/usr/bin/env python3
"""
Version management script for semantic versioning with conventional commits.

This script analyzes git commits since the last tag to determine version bumps
according to conventional commit standards:
- feat: -> minor version bump
- fix: -> patch version bump
- BREAKING CHANGE -> major version bump

Usage:
    python scripts/version_manager.py bump [--dry-run]
    python scripts/version_manager.py get-current-version
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple


class VersionManager:
    def __init__(self, repo_path: Path = None):
        self.repo_path = repo_path or Path(__file__).parent.parent
        self.pyproject_toml = self.repo_path / "pyproject.toml"
        self.twitter_downloader_py = self.repo_path / "twitter_downloader.py"
        self.init_py = self.repo_path / "__init__.py"

    def run_git_command(self, cmd: list) -> str:
        """Run a git command and return stdout."""
        result = subprocess.run(
            ["git"] + cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()

    def get_current_version(self) -> str:
        """Get the current version from pyproject.toml."""
        with open(self.pyproject_toml, 'r') as f:
            content = f.read()

        match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
        if not match:
            raise ValueError("Could not find version in pyproject.toml")

        return match.group(1)

    def get_last_tag(self) -> Optional[str]:
        """Get the last version tag."""
        try:
            return self.run_git_command(["describe", "--tags", "--abbrev=0"])
        except subprocess.CalledProcessError:
            return None

    def get_commits_since_tag(self, tag: str) -> list:
        """Get commits since the given tag."""
        try:
            commits = self.run_git_command([
                "log", "--oneline", f"{tag}..HEAD"
            ])
            return commits.split('\n') if commits else []
        except subprocess.CalledProcessError:
            return []

    def analyze_commits(self, commits: list) -> str:
        """
        Analyze commits to determine version bump type.

        Returns: 'major', 'minor', or 'patch'
        """
        has_breaking = False
        has_feat = False
        has_fix = False

        for commit in commits:
            # Skip merge commits
            if commit.startswith('Merge'):
                continue

            # Check for BREAKING CHANGE in body
            if 'BREAKING CHANGE' in commit.upper():
                has_breaking = True

            # Check commit message prefix
            if commit.startswith('feat'):
                has_feat = True
            elif commit.startswith('fix'):
                has_fix = True

        if has_breaking:
            return 'major'
        elif has_feat:
            return 'minor'
        elif has_fix:
            return 'patch'
        else:
            return 'patch'  # default to patch if no conventional commits

    def bump_version(self, current_version: str, bump_type: str) -> str:
        """Bump the version according to semantic versioning."""
        major, minor, patch = map(int, current_version.split('.'))

        if bump_type == 'major':
            major += 1
            minor = 0
            patch = 0
        elif bump_type == 'minor':
            minor += 1
            patch = 0
        elif bump_type == 'patch':
            patch += 1

        return f"{major}.{minor}.{patch}"

    def update_pyproject_toml(self, new_version: str) -> None:
        """Update version in pyproject.toml."""
        with open(self.pyproject_toml, 'r') as f:
            content = f.read()

        # Update version line
        content = re.sub(
            r'^version\s*=\s*"[^"]*"',
            f'version = "{new_version}"',
            content,
            flags=re.MULTILINE
        )

        with open(self.pyproject_toml, 'w') as f:
            f.write(content)

    def update_twitter_downloader_py(self, new_version: str) -> None:
        """Update __version__ in twitter_downloader.py."""
        with open(self.twitter_downloader_py, 'r') as f:
            content = f.read()

        # Update __version__ line
        content = re.sub(
            r'^__version__\s*=\s*"[^"]*"',
            f'__version__ = "{new_version}"',
            content,
            flags=re.MULTILINE
        )

        with open(self.twitter_downloader_py, 'w') as f:
            f.write(content)

    def update_init_py(self, new_version: str) -> None:
        """Update or create __version__ in __init__.py."""
        init_content = f'__version__ = "{new_version}"\n'

        with open(self.init_py, 'w') as f:
            f.write(init_content)

    def commit_and_tag(self, new_version: str, dry_run: bool = False) -> None:
        """Commit version changes and create tag."""
        if dry_run:
            print(f"[DRY RUN] Would commit and tag version {new_version}")
            return

        # Add files
        self.run_git_command(["add", "pyproject.toml", "twitter_downloader.py", "__init__.py"])

        # Commit
        self.run_git_command([
            "commit", "-m",
            f"chore: bump version to {new_version}"
        ])

        # Create tag
        self.run_git_command([
            "tag", "-a", f"v{new_version}", "-m",
            f"Release version {new_version}"
        ])

    def bump(self, dry_run: bool = False) -> str:
        """Main bump function."""
        current_version = self.get_current_version()
        last_tag = self.get_last_tag()

        if last_tag:
            commits = self.get_commits_since_tag(last_tag)
        else:
            # If no tags, get all commits
            commits = self.run_git_command(["log", "--oneline"]).split('\n')

        if not commits:
            print("No new commits since last tag. Skipping version bump.")
            return current_version

        bump_type = self.analyze_commits(commits)
        new_version = self.bump_version(current_version, bump_type)

        print(f"Current version: {current_version}")
        print(f"Commits analyzed: {len(commits)}")
        print(f"Bump type: {bump_type}")
        print(f"New version: {new_version}")

        if dry_run:
            print("[DRY RUN] Would update files and create tag")
            return new_version

        # Update files
        self.update_pyproject_toml(new_version)
        self.update_twitter_downloader_py(new_version)
        self.update_init_py(new_version)

        # Commit and tag
        self.commit_and_tag(new_version, dry_run)

        print(f"Successfully bumped to version {new_version}")
        return new_version


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Version management script")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # bump command
    bump_parser = subparsers.add_parser("bump", help="Bump version based on commits")
    bump_parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")

    # get-current-version command
    subparsers.add_parser("get-current-version", help="Get current version")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = VersionManager()

    if args.command == "bump":
        try:
            new_version = manager.bump(dry_run=args.dry_run)
            if args.dry_run:
                print(f"New version would be: {new_version}")
            else:
                print(f"Version bumped to: {new_version}")
        except Exception as e:
            print(f"Error during version bump: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "get-current-version":
        try:
            version = manager.get_current_version()
            print(version)
        except Exception as e:
            print(f"Error getting current version: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()