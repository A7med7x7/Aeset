# Developer Testing Guide

This document outlines the testing workflow, guidelines, and pre-release checklist for developers contributing to **Aeset**.

## 1. Development Environment Setup

Ensure you have Python 3.11+ installed on macOS.

```bash
# 1. Clone the repository and navigate into the project directory
git clone https://github.com/a7med7x7/aeset.git aeset
cd aeset

# 2. Install the package in editable mode with development dependencies
pip install -e .
pip install build twine
```

Editable mode (`pip install -e .`) links the `aeset` command directly to your local source code, so any code changes in `aeset/` take effect immediately without re-installing.

## 2. Automated Unit Tests

Unit tests are located in [`tests/test_aeset.py`](../tests/test_aeset.py). They test core functionality without requiring After Effects to be open.

### Running All Tests
```bash
python3 -m unittest discover -s tests -v
```

### Running Specific Test Suites
```bash
# Test After Effects detection and launcher logic
python3 -m unittest tests.test_aeset.TestAesetLauncher -v

# Test folder scaffolding and JSX template generation
python3 -m unittest tests.test_aeset.TestAesetScaffold -v
```

### What Unit Tests Cover:
- **Application Filtering**: Verifies `Render Engine`, `Uninstall`, and non-app directories are excluded from candidate detection.
- **Version Parsing**: Ensures semantic version comparison accurately identifies the newest installed After Effects release.
- **Scaffolding Structure**: Confirms all standard directories (`footage/`, `assets/`, `exports/`, `project/`) are properly created.
- **JSX Generation**: Validates ExtendScript syntax, project parameters, path escaping, and save commands.
- **README Generation**: Validates metadata formatting and dynamic project notes.

## 3. Integration & Manual Testing

### A. Dry-Run Scaffolding (`--no-launch`)
Use `--no-launch` to test CLI prompts, folder creation, and JSX generation without launching After Effects:

```bash
aeset --no-launch
# or
python3 -m aeset.cli --no-launch
```

**Verification Checklist:**
1. Folder `<ProjectName>/` is created in current working directory.
2. Structure matches standard studio conventions:
   - `project/setup.jsx` exists and is formatted properly.
   - `footage/` (`video/`, `audio/`, `renders/`) exists.
   - `assets/` (`images/`, `fonts/`, `documents/`) exists.
   - `exports/` (`drafts/`, `final/`) exists.
   - `README.md` contains the selected resolution, fps, duration, and color space.

### B. End-to-End Live Testing with After Effects
Test the full pipeline including AppleScript execution and ExtendScript project initialization:

```bash
aeset
```

**Verification Checklist:**
1. **Detection**: The CLI identifies your installed After Effects version (e.g. `Adobe After Effects 2024` or `Adobe After Effects 2022`).
2. **Launch**: After Effects launches automatically without any version conflict error dialog.
3. **AppleScript Handshake**: The CLI polls until After Effects is ready and triggers `setup.jsx`.
4. **Project Setup**:
   - Bins `_COMPS`, `_FOOTAGE`, `_ASSETS`, and `_AUDIO` are visible in the Project Panel.
   - Main composition is created with the exact resolution, frame rate, and duration selected.
   - Main composition opens active in the Composition Viewer.
   - Project is automatically saved as `<ProjectName>/project/<ProjectName>.aep`.

## 4. macOS Permissions & Troubleshooting

### AppleScript Automation Permissions
When running `aeset` with live After Effects for the first time, macOS may prompt for permission:
> *"Terminal / VS Code would like to control Adobe After Effects."*

- Click **Allow / OK**.
- If denied, enable it manually in:
  **System Settings > Privacy & Security > Automation > [Your Terminal / IDE] > Adobe After Effects**.

### Cold Launch Timeouts
If After Effects is cold-booting (first launch after restart or plugin scan), it may take longer than usual. The launcher polls for readiness for up to 60 seconds.

## 5. Pre-Release & Packaging Checklist

Before creating a new release or publishing to PyPI:

1. **Run Unit Tests**:
   ```bash
   python3 -m unittest discover -s tests -v
   ```

2. **Sync Version Numbers**:
   Ensure the version is bumped and matches in both files:
   - `pyproject.toml` (`version = "x.y.z"`)
   - `aeset/__init__.py` (`__version__ = "x.y.z"`)

3. **Build the Distribution Packages**:
   ```bash
   python3 -m build
   ```

4. **Verify Package Contents**:
   ```bash
   # Check sdist contents
   tar -tzf dist/*.tar.gz

   # Check wheel contents
   unzip -l dist/*.whl
   ```
   *Ensure no unwanted `.aep`, cache files, or temporary artifacts are included in the build.*

5. **Validate Package Metadata with Twine**:
   ```bash
   twine check dist/*
   ```

6. **Tag and Push**:
   ```bash
   git tag v0.1.2
   git push origin main --tags
   ```