import click

from cigen.adapter.input.github_command.action_command import (version_format_param, on_events,
                                                               on_branch_validate_param,
                                                               action_format_param, mapping_instance_action,
                                                               action_params_valid, confirm_generation_action)
from cigen.core.github.github_action import OnEventFactory
from cigen.core.github.nodejs_action import ActionCIGenNodejs, NodejsActionBuilderImpl

ACTION_DOC_LONG = """
        Actions:
        0 - base 1 - base_version_list 2 - checkout 3 - setup_node 4 - setup_node_with_version_list 5 -
        install_dependencies 6 - run_tests

        base ou base_version_list 0 ou 1 is required like last parameter
                    :example: 2,3,5 0
        """


@click.command("nodejs", help="Generate a NodeJS action", epilog=ACTION_DOC_LONG)
@click.option("-n", "--name", nargs=1, help="Name of the action", prompt="Name of the action", required=True)
@click.option("-b", "--branch_name", help="Branch to add", prompt="Name of the branch", required=True)
@click.option("-a", "--action", help="Action to add", prompt="Action to add", required=True)
@click.option("-v", "--version", nargs=1, help="Version of NodeJS [default=14.x]", type=click.STRING, default="14.x",
              required=False)
def action_nodejs(name, branch_name, action, version):
    version = version_format_param(version)

    on_branch_validate_param(branch_name)

    on_event = OnEventFactory.create_events(on_events(branch_name.split(",")))
    action_ciGen_nodejs = ActionCIGenNodejs()
    action_ciGen_nodejs.builder = NodejsActionBuilderImpl(name, version, on_event)

    elements, lastElement = action_format_param(action)

    for actions in elements:
        if actions.isnumeric():
            actions = int(actions)
            action_ciGen_nodejs = action_builder(action_ciGen_nodejs, actions)

    ciGen = action_params_valid(elements, lastElement, action_ciGen_nodejs, action)

    confirm_generation_action(ciGen, name)


def action_builder(action_ciGen_nodejs, actions) -> ActionCIGenNodejs:
    action_mapping = {
        "build_base": {
            "action_id": 1,
            "steps": [
                action_ciGen_nodejs.build_base
            ]
        },
        "build_base_with_version_list": {
            "action_id": 2,
            "steps": [
                action_ciGen_nodejs.build_base_with_version_list
            ]
        },
        "checkout": {
            "action_id": 3,
            "steps": [
                action_ciGen_nodejs.builder.step_checkout
            ]
        },
        "setup_node": {
            "action_id": 4,
            "steps": [
                action_ciGen_nodejs.builder.step_setup_node
            ]
        },
        "setup_node_with_version_list": {
            "action_id": 5,
            "steps": [
                action_ciGen_nodejs.builder.step_setup_node_with_version_matrix
            ]
        },
        "install_dependencies": {
            "action_id": 6,
            "steps": [
                action_ciGen_nodejs.builder.step_install_dependencies
            ]
        },
        "run_tests": {
            "action_id": 7,
            "steps": [
                action_ciGen_nodejs.builder.step_test
            ]
        }
    }

    mapping_instance_action(action_mapping, actions)

    return action_ciGen_nodejs


