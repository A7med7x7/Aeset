import pathlib
import shutil
import sys
from datetime import datetime

import click
import questionary
from questionary import Style

from .launcher import detect_ae_version, launch_after_effects, run_jsx_via_applescript
from .scaffold import create_project_folders, generate_jsx, generate_readme

custom_style = Style([
    ("questionmark", "fg:#00bcd4 bold"),
])


def _ask(prompt):
    """Run a questionary prompt; exit cleanly if the user cancels (Ctrl+C / Esc)."""
    answer = prompt.ask()
    if answer is None:
        click.echo("Aborted.")
        sys.exit(0)
    return answer


@click.command()
@click.option('--no-launch', is_flag=True, help="Create the project but do not launch After Effects.")
def main(no_launch):
    """Aeset — After Effects Project Scaffolding Tool."""

    if sys.platform != "darwin":
        click.echo(click.style(
            "aeset is macOS-only — it relies on AppleScript and the `open` command.",
            fg="red", bold=True,
        ))
        sys.exit(1)

    click.echo(click.style("""\n Aeset — After Effects Project Scaffolder\n
     █████  ███████ ███████ ███████ ████████
    ██   ██ ██      ██      ██         ██
    ███████ █████   ███████ █████      ██
    ██   ██ ██           ██ ██         ██
    ██   ██ ███████ ███████ ███████    ██

    """, fg="cyan", bold=True))

    ae_version = detect_ae_version()
    if not no_launch and ae_version is None:
        click.echo(click.style(
            "Adobe After Effects was not found in /Applications. "
            "Re-run with --no-launch to scaffold without opening AE.",
            fg="red",
        ))
        sys.exit(1)

    project_name = _ask(questionary.text(
        "Project name",
        validate=lambda text: len(text) > 0 or "Project name cannot be empty.",
        qmark="🎬",
        style=custom_style,
    ))

    project_type = _ask(questionary.select(
        "Project type",
        choices=["Commercial", "Personal", "Motion Test", "Music Video"],
        qmark="🎬",
        style=custom_style,
    ))

    resolution = _ask(questionary.select(
        "Resolution",
        choices=[
            "1920×1080 (Full HD)",
            "3840×2160 (4K)",
            "1080×1080 (Square / Instagram)",
            "1080×1920 (Vertical / Reels)",
        ],
        qmark="🎬",
        style=custom_style,
    )).split(" ")[0]

    fps = int(_ask(questionary.select(
        "Frame rate",
        choices=["24", "25", "30", "60"],
        qmark="🎬",
        style=custom_style,
    )))

    duration = int(_ask(questionary.text(
        "Duration (seconds)",
        default="10",
        validate=lambda text: text.isdigit() or "Duration must be an integer.",
        qmark="🎬",
        style=custom_style,
    )))

    color_space = _ask(questionary.select(
        "Color space",
        choices=["sRGB", "Rec. 709", "ACES"],
        qmark="🎬",
        style=custom_style,
    ))

    project_path = pathlib.Path.cwd() / project_name
    if project_path.exists():
        if not _ask(questionary.confirm(
            f"Directory {project_name} already exists. Overwrite?",
            qmark="🎬",
            style=custom_style,
        )):
            click.echo("Aborted.")
            return
        shutil.rmtree(project_path)

    config = {
        "type": project_type,
        "resolution": resolution,
        "fps": fps,
        "duration": duration,
        "color_space": color_space,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    click.echo(f"✔ Creating {project_name}/...")
    create_project_folders(project_path)

    click.echo("✔ Generating composition config...")
    jsx_path = generate_jsx(project_path, project_name, config)

    click.echo("✔ Generating README.md...")
    generate_readme(project_path, project_name, config)

    if not no_launch:
        click.echo(f"✔ Opening After Effects ({ae_version})...")
        if launch_after_effects(ae_version):
            click.echo("✔ Waiting for After Effects to be ready...")
            if run_jsx_via_applescript(jsx_path, ae_version):
                click.echo("✔ Project and composition initialized in After Effects.")
            else:
                click.echo(click.style("✘ Could not run setup script in After Effects.", fg="yellow"))
        else:
            click.echo(click.style("✘ Could not launch After Effects automatically.", fg="red"))
    else:
        click.echo(click.style(
            "ℹ To initialize the project later, open After Effects and run:\n"
            f"  File > Scripts > Run Script File... -> select {project_name}/project/setup.jsx",
            fg="yellow",
        ))

    click.echo(click.style(f"\n🎉 Done! Project {project_name} is ready.\n", fg="green", bold=True))


if __name__ == "__main__":
    main()
