import pathlib
import subprocess


def detect_ae_version() -> str | None:
    """Return the newest installed Adobe After Effects bundle name, or None if not found."""
    candidates = sorted(
        pathlib.Path("/Applications").glob("Adobe After Effects */Adobe After Effects *.app"),
        reverse=True,
    )
    if not candidates:
        # Some installs place the .app directly in /Applications
        candidates = sorted(
            pathlib.Path("/Applications").glob("Adobe After Effects *.app"),
            reverse=True,
        )
    return candidates[0].stem if candidates else None


def launch_after_effects(aep_path: pathlib.Path, ae_version: str) -> bool:
    """Launches After Effects and opens the specified .aep file."""
    try:
        subprocess.run(["open", str(aep_path.resolve()), "-a", ae_version], check=True)
        return True
    except Exception as e:
        print(f"Error opening project: {e}")
        return False


def _wait_for_ae_ready(ae_version: str, timeout_seconds: int = 60) -> bool:
    """Poll AE via AppleScript DoScript until it responds, or timeout."""
    iterations = timeout_seconds * 2  # 0.5s per iteration
    script = (
        f'repeat {iterations} times\n'
        f'    try\n'
        f'        tell application "{ae_version}" to DoScript "1"\n'
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
        f'tell application "{ae_version}" to '
        f'DoScript "{_escape_for_applescript_string(js_to_run)}"'
    )

    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running AppleScript: {e}")
        return False
