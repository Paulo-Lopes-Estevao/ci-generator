import click

from cigen.adapter.input.github_command.action_command import on_events, version_format_param, \
    confirm_generation_action, action_format_param, action_params_valid, on_branch_validate_param, \
    mapping_instance_action
from cigen.core.github.github_action import OnEventFactory
from cigen.core.github.go_action import GoActionBuilderImpl, ActionCIGenGolang

ACTION_DOC_LONG = """
        Actions:
        0 - base 2 - version_list 3 - build_base_with_version_list 4 - checkout 5 - setup_go 6 -
        setup_go_with_version_list 7 - build 8 - cache 9 - install_dependencies 10 - tests 11 - tests_and_coverage
        12 - tests_and_coverage_with_coverage 13 - tests_and_coverage_with_coverage_and_html 14 -
        tests_and_coverage_with_coverage_and_html_and_upload

        base ou version_list 0 ou 1 is required like last parameter
                 :example: 2,3,5 0
        """


@click.command("go", help="Generate action github actions for go", epilog=ACTION_DOC_LONG)
@click.option("-n", "--name", nargs=1, help="Name of the action", prompt="Name of the action", required=True)
@click.option("-b", "--branch_name", help="Branch to add", prompt="Name of the branch", required=True)
@click.option("-a", "--action", help="Action to add", prompt="Action to add", required=True)
@click.option("-v", "--version", nargs=1, help="Version of go [default=1.17]", type=click.STRING, default="1.17",
              required=False)
def action_go(name, branch_name, action, version):
    version = version_format_param(version)

    on_branch_validate_param(branch_name)

    on_event = OnEventFactory.create_events(on_events(branch_name.split(",")))
    action_ciGen_golang = ActionCIGenGolang()
    action_ciGen_golang.builder = GoActionBuilderImpl(name, version, on_event)

    elements, lastElement = action_format_param(action)

    for actions in elements:
        if actions.isnumeric():
            actions = int(actions)
            action_ciGen_golang = action_builder(action_ciGen_golang, actions)

    ciGen = action_params_valid(elements, lastElement, action_ciGen_golang, action)

    confirm_generation_action(ciGen, name)


def action_builder(action_ciGen_golang, actions) -> ActionCIGenGolang:
    action_mapping = {
        "build_base": {
            "action_id": 1,
            "steps": [
                action_ciGen_golang.builder.step_checkout,
                action_ciGen_golang.builder.step_setup_go,
                action_ciGen_golang.builder.step_run_build,
                action_ciGen_golang.builder.step_run_tests,
            ]
        },
        "build_base_with_version_list": {
            "action_id": 2,
            "steps": [
                action_ciGen_golang.builder.step_checkout,
                action_ciGen_golang.builder.step_setup_go_with_versions_matrix,
                action_ciGen_golang.builder.step_run_build,
                action_ciGen_golang.builder.step_run_tests
            ]
        },
        "checkout": {
            "action_id": 3,
            "steps": [
                action_ciGen_golang.builder.step_checkout
            ]
        },
        "setup_go": {
            "action_id": 4,
            "steps": [
                action_ciGen_golang.builder.step_setup_go
            ]
        },
        "setup_go_with_version_list": {
            "action_id": 5,
            "steps": [
                action_ciGen_golang.builder.step_setup_go_with_versions_matrix
            ]
        },
        "build": {
            "action_id": 6,
            "steps": [
                action_ciGen_golang.builder.step_run_build
            ]
        },
        "cache": {
            "action_id": 7,
            "steps": [
                action_ciGen_golang.builder.step_run_cache
            ]
        },
        "install_dependencies": {
            "action_id": 8,
            "steps": [
                action_ciGen_golang.builder.step_run_install_dependencies
            ]
        },
        "tests": {
            "action_id": 9,
            "steps": [
                action_ciGen_golang.builder.step_run_tests
            ]
        },
        "tests_and_coverage": {
            "action_id": 10,
            "steps": [
                action_ciGen_golang.builder.step_run_tests_and_coverage
            ]
        },
        "tests_and_coverage_with_coverage": {
            "action_id": 11,
            "steps": [
                action_ciGen_golang.builder.step_run_tests_and_coverage_with_coverage
            ]
        },
        "tests_and_coverage_with_coverage_and_html": {
            "action_id": 12,
            "steps": [
                action_ciGen_golang.builder.step_run_tests_and_coverage_with_coverage_and_html
            ]
        },
        "tests_and_coverage_with_coverage_and_html_and_upload": {
            "action_id": 13,
            "steps": [
                action_ciGen_golang.builder.step_run_tests_and_coverage_with_coverage_and_html_and_upload
            ]
        }
    }

    mapping_instance_action(action_mapping, actions)

    return action_ciGen_golang
