<div style=text-align:center;>

# Aeset

[![PyPI version](https://img.shields.io/pypi/v/aeset?color=blue)](https://pypi.org/project/aeset/)
[![Status](https://img.shields.io/badge/status-beta-orange)](#)

</div>

![aeset brand](https://raw.githubusercontent.com/A7med7x7/Aeset/main/docs/images/terminal-feel.png)

Every video editor or motion designer wastes 10–20 minutes at the start of every project doing the exact same thing: creating folders by hand, naming them consistently, opening After Effects, and setting up a new composition with the right resolution, framerate, and duration. It is not creative work. It is repetitive work. Multiply it by 50 projects a year and you have lost a full work week to folder creation and blank composition setup.

Aeset is a tool built to solve this for After Effects on macOS. It takes the "scaffolding" logic used by software developers and applies it to the motion design world.


## Installation and Requirements

### Installation
Aeset can be installed via pip:
```bash
pip install aeset
```

### Requirements
- macOS (Intel & Apple Silicon: M1, M2, M3, M4+): AppleScript and the `open` command are macOS-specific.
- Adobe After Effects (Universal: AE 2020 through 2026+)
- Python 3.11+

### Usage

Run the command
```bash
aeset
```
and then you're ready to scaffold your project.


## 1. What The Tool Does

The user opens their terminal, navigates to where they want the project to live, and runs:

```bash
aeset
```

The tool then asks a series of interactive questions:
- Project name (e.g., Nike_Ident_2026)
- Project type (Commercial, Personal, etc.)
- Resolution (Full HD, 4K, Vertical, etc.)
- Frame rate (24, 25, 30, 60 fps)
- Duration in seconds
- Color space (sRGB, Rec. 709, ACES)

After those answers, the tool:
1. Creates a standardized folder tree inside a new project directory.
2. Generates an ExtendScript `.jsx` file tailored to your specifications.
3. Automatically launches your installed version of After Effects.
4. Uses AppleScript to run the `.jsx` setup script, which builds the composition, organizes project bins, and saves a native `.aep` project file.

## 2. Folder Structure Generated

Aeset generates a directory layout that follows conventions used by professional motion studios. The core principle is: never mix source files with outputs.

### On Disk:
```
<ProjectName>/
├── project/
│   ├── <ProjectName>.aep       (native After Effects project)
│   └── setup.jsx               (project initialization script)
├── footage/
│   ├── video/                  (raw video clips)
│   ├── audio/                  (music, SFX, voiceover)
│   └── renders/                (outputs from C4D, Blender, etc.)
├── assets/
│   ├── images/                 (static graphics, PNGs, PSDs, AI files)
│   ├── fonts/                  (local fonts scoped to this project)
│   └── documents/              (briefs, scripts, reference PDFs)
├── exports/
│   ├── drafts/                 (work-in-progress renders)
│   └── final/                  (delivered, approved renders)
└── README.md                   (auto-generated project notes)
```

### Inside After Effects:
The tool also creates corresponding bins in the Project Panel to keep your workspace clean:
- _COMPS (containing your main composition)
- _FOOTAGE
- _ASSETS
- _AUDIO

## 3. The Mechanism

### Dynamic Project Initialization
Instead of shipping a static pre-saved `.aep` binary file that locks you into a specific version, Aeset generates and saves the project directly through After Effects' ExtendScript engine (`app.newProject()` and `app.project.save()`). This guarantees 100% compatibility across all After Effects releases and hardware architectures.

### The .jsx file
The tool generates a plain text ExtendScript file at runtime. This script has full programmatic access to After Effects. It uses the specs you provided in the terminal to build your composition, configure color management, and organize your project panel.

### The AppleScript Trigger
The `.jsx` is triggered explicitly after After Effects opens using a macOS AppleScript command (`DoScript`). This bridges the gap between the Python-based CLI and the Adobe environment.

## 4. Constraints and Assumptions

- No Adobe credentials required: The tool uses only local scripting.
- After Effects must already be installed: The tool detects your installed AE application in `/Applications`.
- Local execution: All files are generated and stored locally on your machine.


## 5. Development & Testing

For guidelines on local testing, running automated test suites, manual verification, and the pre-release checklist, see the [Developer Testing Guide](docs/TESTING.md).

