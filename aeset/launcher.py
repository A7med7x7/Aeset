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
    # Use absolute path and ensure it's escaped for JavaScript
    script_path = str(jsx_path.absolute())
    
    # We send a piece of JavaScript code to AE: $.evalFile("/path/to/script.jsx");
    js_to_run = f"$.evalFile('{script_path}');"
    applescript = f'tell application "{ae_version}" to DoScript "{js_to_run}"'
    
    try:
        # Give AE a moment to open/load the project before sending the command
        time.sleep(10) 
        subprocess.run(["osascript", "-e", applescript], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running AppleScript: {e}")
        return False
