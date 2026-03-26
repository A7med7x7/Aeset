import subprocess
import time
import pathlib

def launch_after_effects(aep_path: pathlib.Path, ae_version: str = "Adobe After Effects 2025"):
    """Launches After Effects with the specified .aep file."""
    try:
        # Launch After Effects with the project file
        subprocess.Popen(["open", "-a", ae_version, str(aep_path)])
        return True
    except Exception as e:
        print(f"Error launching After Effects: {e}")
        return False

def run_jsx_via_applescript(jsx_path: pathlib.Path, ae_version: str = "Adobe After Effects 2025"):
    """Triggers a .jsx script in After Effects using AppleScript."""
    # Escape path for AppleScript
    script_path = str(jsx_path.absolute())
    
    # AppleScript command
    applescript = f'tell application "{ae_version}" to do script "{script_path}"'
    
    try:
        # Give AE a moment to open before sending the command
        time.sleep(5) 
        subprocess.run(["osascript", "-e", applescript], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running AppleScript: {e}")
        return False
