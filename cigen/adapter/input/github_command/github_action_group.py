import click
from cigen.adapter.input.github_command.go_command import action_go
from cigen.adapter.input.github_command.nodejs_command import action_nodejs


@click.group()
def github_action():
    """
    This is the main command for the GitHub Actions
    """
    pass


github_action.add_command(action_go)
github_action.add_command(action_nodejs)
