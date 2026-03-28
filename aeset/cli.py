import click
import questionary
import pathlib
from datetime import datetime
from .scaffold import create_project_folders, generate_jsx, copy_template_aep, generate_readme
from .launcher import launch_after_effects, run_jsx_via_applescript

@click.command()
@click.option('--no-launch', is_flag=True, help="Create the project but do not launch After Effects.")
def main(no_launch):
    """Aeset — After Effects Project Scaffolding Tool."""
    
    click.echo(click.style("\n Aeset — After Effects Project Scaffolder\n", fg="cyan", bold=True))

    # 1. Collect inputs
    project_name = questionary.text(
        "Project name",
        validate=lambda text: len(text) > 0 or "Project name cannot be empty."
    ).ask()
    
    if not project_name:
        return

    project_type = questionary.select(
        "Project type",
        choices=["Commercial", "Personal", "Motion Test", "Music Video"]
    ).ask()

    resolution = questionary.select(
        "Resolution",
        choices=[
            "1920×1080 (Full HD)",
            "3840×2160 (4K)",
            "1080×1080 (Square / Instagram)",
            "1080×1920 (Vertical / Reels)"
        ]
    ).ask()
    # Clean up resolution choice
    resolution = resolution.split(" ")[0]

    fps = questionary.select(
        "Frame rate",
        choices=["24", "25", "30", "60"]
    ).ask()
    fps = int(fps)

    duration = questionary.text(
        "Duration (seconds)",
        default="10",
        validate=lambda text: text.isdigit() or "Duration must be an integer."
    ).ask()
    duration = int(duration)

    color_space = questionary.select(
        "Color space",
        choices=["sRGB", "Rec. 709", "ACES"]
    ).ask()

    # Create project directory
    project_path = pathlib.Path.cwd() / project_name
    if project_path.exists():
        if not questionary.confirm(f"Directory {project_name} already exists. Overwrite?").ask():
            click.echo("Aborted.")
            return

    # 2. Scaffolding
    config = {
        "type": project_type,
        "resolution": resolution,
        "fps": fps,
        "duration": duration,
        "color_space": color_space,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    click.echo(f"✔ Creating {project_name}/...")
    create_project_folders(project_path)
    
    click.echo("✔ Copying project template...")
    aep_path = copy_template_aep(project_path, project_name)
    
    click.echo("✔ Generating composition config...")
    jsx_path = generate_jsx(project_path, project_name, config)
    
    click.echo("✔ Generating README.md...")
    generate_readme(project_path, project_name, config)

    # 3. Launch
    if not no_launch:
        click.echo("✔ Opening After Effects...")
        if launch_after_effects(aep_path):
            click.echo("✔ Triggering setup script...")
            run_jsx_via_applescript(jsx_path)
        else:
            click.echo(click.style("✘ Could not launch After Effects automatically.", fg="red"))
    
    click.echo(click.style(f"\n🎉 Done! Project {project_name} is ready.\n", fg="green", bold=True))

if __name__ == "__main__":
    main()