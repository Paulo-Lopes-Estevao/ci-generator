import click
from cigen.adapter.input.github_command import github_action_group
from cigen.adapter.input.gitlab_command import gitlab_group
from cigen.adapter.input.jenkins_command import jenkins_group
from cigen.adapter.input.docker_command import docker_group



@click.group()
def cli():
    """
    ciGen is a Continuous Integration Generator
    """
    pass


cli.add_command(github_action_group.github_action)
cli.add_command(gitlab_group.gitlab)
cli.add_command(jenkins_group.jenkins)
cli.add_command(docker_group.docker)
