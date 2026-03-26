import subprocess
import time
import pathlib

def launch_after_effects(aep_path: pathlib.Path, ae_version: str = "Adobe After Effects 2025"):
    """Launches After Effects and opens the specified .aep file."""
    abs_path = str(aep_path.resolve())
    
    # Use 'open' command which is usually most reliable for launching with a file
    try:
        subprocess.run(["open", abs_path, "-a", ae_version], check=True)
        return True
    except Exception as e:
        print(f"Error opening project: {e}")
        return False

def run_jsx_via_applescript(jsx_path: pathlib.Path, ae_version: str = "Adobe After Effects 2025"):
    """Triggers a .jsx script in After Effects using AppleScript DoScript."""
    script_path = str(jsx_path.absolute())
    
    # Use DoScript (one word) which is the standard AE AppleScript command
    applescript = f'tell application "{ae_version}" to DoScript "{script_path}"'
    
    try:
        # Give AE a moment to open/load the project before sending the command
        time.sleep(10) 
        subprocess.run(["osascript", "-e", applescript], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running AppleScript: {e}")
        return False
