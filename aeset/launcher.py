import subprocess
import time
import pathlib

def launch_after_effects(aep_path: pathlib.Path, ae_version: str = "Adobe After Effects 2025"):
    """Launches After Effects with the specified .aep file."""
    try:
        # Use resolve() to get absolute path
        abs_path = str(aep_path.resolve())
        # Launch After Effects with the project file
        # Sometimes 'open <file> -a <app>' is more reliable
        subprocess.run(["open", abs_path, "-a", ae_version], check=True)
        return True
    except Exception as e:
        print(f"Error launching After Effects: {e}")
        return False

def run_jsx_via_applescript(jsx_path: pathlib.Path, ae_version: str = "Adobe After Effects 2025"):
    """Triggers a .jsx script in After Effects using AppleScript."""
    # Escape path for AppleScript
    script_path = str(jsx_path.absolute())
    
    # AppleScript command - activate first to ensure AE is responsive
    applescript = f'''
    tell application "{ae_version}"
        activate
        do script "{script_path}"
    end tell
    '''
    
    try:
        # Give AE a moment to open before sending the command
        # 15 seconds might be safer for AE to fully load the project
        time.sleep(15) 
        subprocess.run(["osascript", "-e", applescript], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running AppleScript: {e}")
        return False
