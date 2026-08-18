import pathlib
import plistlib
import re
import subprocess


def _parse_version(app_path: pathlib.Path) -> tuple:
    """Extract a version tuple from Info.plist or folder/app name for sorting."""
    plist_path = app_path / "Contents" / "Info.plist"
    if plist_path.exists():
        try:
            with open(plist_path, "rb") as f:
                pl = plistlib.load(f)
                ver_str = pl.get("CFBundleShortVersionString") or pl.get("CFBundleVersion") or ""
                nums = [int(n) for n in re.findall(r"\d+", ver_str)]
                if nums:
                    return tuple(nums)
        except Exception:
            pass
    # Fallback to numbers found in the app or folder name
    nums = [int(n) for n in re.findall(r"\d+", app_path.as_posix())]
    return tuple(nums) if nums else (0,)


def _is_valid_ae_app(app_path: pathlib.Path) -> bool:
    """Filter out render engine, uninstaller, and non-app files."""
    name_lower = app_path.name.lower()
    if "render engine" in name_lower or "uninstall" in name_lower:
        return False
    return name_lower.startswith("adobe after effects") and app_path.suffix == ".app"


def detect_ae_app_path() -> pathlib.Path | None:
    """Return the Path to the newest installed Adobe After Effects .app bundle, or None."""
    patterns = [
        "/Applications/Adobe After Effects */Adobe After Effects *.app",
        "/Applications/Adobe After Effects *.app",
        "/Applications/Adobe After Effects*/**/Adobe After Effects*.app",
    ]
    candidates = set()
    for pattern in patterns:
        for p in pathlib.Path("/").glob(pattern.lstrip("/")):
            if _is_valid_ae_app(p):
                candidates.add(p)

    if not candidates:
        return None

    sorted_candidates = sorted(candidates, key=_parse_version, reverse=True)
    return sorted_candidates[0]


def detect_ae_version() -> str | None:
    """Return the newest installed Adobe After Effects bundle name, or None if not found."""
    app_path = detect_ae_app_path()
    return app_path.stem if app_path else None


def launch_after_effects(ae_version: str | pathlib.Path, aep_path: pathlib.Path | None = None) -> bool:
    """Launches After Effects."""
    try:
        cmd = ["open"]
        if aep_path and pathlib.Path(aep_path).exists():
            cmd.append(str(pathlib.Path(aep_path).resolve()))
        cmd.extend(["-a", str(ae_version)])
        subprocess.run(cmd, check=True)
        return True
    except Exception as e:
        print(f"Error launching After Effects: {e}")
        return False


def _wait_for_ae_ready(ae_version: str, timeout_seconds: int = 60) -> bool:
    """Poll AE via AppleScript DoScript until it responds, or timeout."""
    iterations = timeout_seconds * 2  # 0.5s per iteration
    escaped_ae = _escape_for_applescript_string(ae_version)
    script = (
        f'repeat {iterations} times\n'
        f'    try\n'
        f'        tell application "{escaped_ae}" to DoScript "1"\n'
        f'        return "ready"\n'
        f'    on error\n'
        f'        delay 0.5\n'
        f'    end try\n'
        f'end repeat\n'
        f'return "timeout"\n'
    )
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=timeout_seconds + 5,
        )
        return result.stdout.strip() == "ready"
    except subprocess.TimeoutExpired:
        return False


def _escape_for_js_single_quoted(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'")


def _escape_for_applescript_string(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def run_jsx_via_applescript(jsx_path: pathlib.Path, ae_version: str) -> bool:
    """Triggers a .jsx script in After Effects using AppleScript DoScript."""
    if not _wait_for_ae_ready(ae_version):
        print("Warning: After Effects did not become ready in time; trying anyway.")

    script_path = str(jsx_path.absolute())
    js_to_run = f"$.evalFile('{_escape_for_js_single_quoted(script_path)}');"
    applescript = (
        f'tell application "{_escape_for_applescript_string(ae_version)}" to '
        f'DoScript "{_escape_for_applescript_string(js_to_run)}"'
    )

    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running AppleScript: {e}")
        return False
