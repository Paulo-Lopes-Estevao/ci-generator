import os
from pathlib import Path

import click
import yaml


def verify_folder_exists(path: Path) -> bool:
    return path.exists()


def create_folder(path: Path) -> None:
    print("Creating folder...", path)
    path.mkdir(parents=True, exist_ok=True)


def create_file(path: Path, content) -> None:
    content_yml = yaml.dump(content, sort_keys=False, default_flow_style=False).replace('\'on\':', 'on:')
    path.write_text(content_yml)


def verify_file_exists(path: Path, content) -> None:
    if path.exists():
        confirm = click.confirm("Do you want to overwrite the file?")
        if confirm:
            print("Overwriting file...")
            path.unlink()
            create_file(path, content)
        else:
            click.echo("Aborted!")
            return


def generate_action(path, content) -> None:
    pathFile = Path(path)
    if verify_folder_exists(pathFile):
        verify_file_exists(pathFile, content)
    else:
        create_folder(Path(os.path.dirname(path)))
        create_file(pathFile, content)
