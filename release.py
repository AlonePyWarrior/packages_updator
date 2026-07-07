#!/usr/bin/env python
"""
Release helper for py-pkg-updater.

Usage:
    python release.py 0.1.5

This script:
- updates package version
- builds and checks the package locally
- commits the release
- creates a Git tag
- pushes main and the tag to GitHub

The tag push triggers GitHub Actions, which publishes to PyPI.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path


PACKAGE_DIR = Path("update-python-packages")
PYPROJECT = PACKAGE_DIR / "pyproject.toml"
INIT_FILE = PACKAGE_DIR / "src" / "update_python_packages" / "__init__.py"
BRANCH = "main"


def run(cmd: list[str], cwd: Path | None = None) -> str:
    print(f"\n> {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )

    if result.stdout:
        print(result.stdout.strip())

    if result.stderr:
        print(result.stderr.strip())

    if result.returncode != 0:
        raise SystemExit(f"\nCommand failed: {' '.join(cmd)}")

    return result.stdout.strip()


def ensure_repo_root() -> Path:
    root = Path(run(["git", "rev-parse", "--show-toplevel"]))
    return root


def ensure_clean_worktree() -> None:
    status = run(["git", "status", "--porcelain"])
    if status:
        raise SystemExit(
            "\nYour Git working tree is not clean.\n"
            "Commit or discard your changes before running the release script."
        )


def validate_version(version: str) -> None:
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise SystemExit(
            "\nInvalid version format.\n"
            "Use semantic version format like: 0.1.5"
        )


def replace_version_in_file(path: Path, pattern: str, replacement: str) -> None:
    text = path.read_text(encoding="utf-8")
    new_text, count = re.subn(pattern, replacement, text, count=1)

    if count != 1:
        raise SystemExit(f"\nCould not update version in: {path}")

    path.write_text(new_text, encoding="utf-8")


def remove_if_exists(path: Path) -> None:
    if path.exists():
        print(f"Removing {path}")
        shutil.rmtree(path)


def ensure_tag_does_not_exist(tag: str) -> None:
    local_tags = run(["git", "tag", "--list", tag])
    if local_tags:
        raise SystemExit(f"\nLocal tag already exists: {tag}")

    remote_tags = run(["git", "ls-remote", "--tags", "origin", tag])
    if remote_tags:
        raise SystemExit(f"\nRemote tag already exists: {tag}")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("\nUsage: python release.py 0.1.5")

    version = sys.argv[1].strip()
    tag = f"v{version}"

    validate_version(version)

    repo_root = ensure_repo_root()
    print(f"\nRepo root: {repo_root}")

    if Path.cwd().resolve() != repo_root.resolve():
        print(f"Changing directory to repo root: {repo_root}")
        # subprocess cwd handles commands; file paths are resolved from repo root below

    ensure_clean_worktree()

    current_branch = run(["git", "branch", "--show-current"], cwd=repo_root)
    if current_branch != BRANCH:
        raise SystemExit(f"\nYou are on branch '{current_branch}'. Switch to '{BRANCH}' first.")

    ensure_tag_does_not_exist(tag)

    run(["git", "pull", "--rebase", "origin", BRANCH], cwd=repo_root)

    pyproject_path = repo_root / PYPROJECT
    init_path = repo_root / INIT_FILE

    if not pyproject_path.exists():
        raise SystemExit(f"\nMissing file: {pyproject_path}")

    if not init_path.exists():
        raise SystemExit(f"\nMissing file: {init_path}")

    print(f"\nUpdating version to {version}")

    replace_version_in_file(
        pyproject_path,
        r'version\s*=\s*"[^"]+"',
        f'version = "{version}"',
    )

    replace_version_in_file(
        init_path,
        r'__version__\s*=\s*"[^"]+"',
        f'__version__ = "{version}"',
    )

    remove_if_exists(repo_root / PACKAGE_DIR / "dist")
    remove_if_exists(repo_root / PACKAGE_DIR / "build")
    remove_if_exists(repo_root / PACKAGE_DIR / "src" / "py_pkg_updater.egg-info")

    run([sys.executable, "-m", "build"], cwd=repo_root / PACKAGE_DIR)
    run([sys.executable, "-m", "twine", "check", "dist/*"], cwd=repo_root / PACKAGE_DIR)

    run(["git", "add", str(PYPROJECT), str(INIT_FILE)], cwd=repo_root)
    run(["git", "commit", "-m", f"Release {version}"], cwd=repo_root)
    run(["git", "tag", tag], cwd=repo_root)
    run(["git", "push", "origin", BRANCH], cwd=repo_root)
    run(["git", "push", "origin", tag], cwd=repo_root)

    print("\nRelease started successfully.")
    print(f"GitHub Actions: https://github.com/AlonePyWarrior/packages_updator/actions")
    print(f"PyPI: https://pypi.org/project/py-pkg-updater/{version}/")


if __name__ == "__main__":
    main()