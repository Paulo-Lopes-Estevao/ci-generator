import pprint

import click

from cigen.adapter.output.github_out.file_action import generate_action
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


def action_params_valid(action_ciGen_golang, action):
    action_ciGen = None
    lastElement = action.split(" ")[len(action.split(" ")) - 1]

    dropLastElement = action.split(" ")
    if len(dropLastElement) > 1:
        dropLastElement.pop()
        dropLastElement = dropLastElement[0].split(",")

    elements = dropLastElement

    if "2" in elements or "1" in elements:
        if len(elements) > 1:
            click.echo("""
                    The action after the value 1 or 2 is [optional] the last value after is a base action of a simple code.
                    The action 1 or 2 cannot be followed by any value separated by a comma. the last parameter is [optional] base.

                    Example: 1 or 2 - is valid
                    Example: 1 0 or 2 1 - is valid
                    Example: 1,2 0 or 2,3 1 - is invalid 
                    """)
            return
    else:
        if len(action.split(",")) == 1:
            click.echo("Action required 2 parameters! Example: 3,4,6 0")
            return

    for actions in elements:
        if actions.isnumeric():
            actions = int(actions)
        action_ciGen = action_builder(action_ciGen_golang, actions)

    if lastElement == "0" or elements[0] == "1":
        click.echo(pprint.pprint(action_ciGen.action_build_base()))
        return action_ciGen.action_build_base()
    elif lastElement == "1" or elements[0] == "2":
        click.echo(pprint.pprint(action_ciGen.action_build_base_with_version_list()))
        return action_ciGen.action_build_base_with_version_list()
    else:
        click.echo("Action not found")
        return


def on_events(listEvent: list[str]) -> dict:
    OnEventsName = {}
    branchesName = {}

    if len(listEvent) == 1:
        names = listEvent[0].split(" ")
        branchesName['branches'] = [names[1]]
        OnEventsName[names[0]] = branchesName
        return OnEventsName

    if len(listEvent) == 2:
        branchesName['branches'] = listEvent[1].split(",")
        OnEventsName[listEvent[0]] = branchesName
        return OnEventsName

    countElements = 0
    for i in range(len(listEvent)):
        if countElements >= len(listEvent):
            break

        branchesName['branches'] = listEvent[countElements + 1].split(",")
        OnEventsName[listEvent[countElements]] = branchesName
        countElements += 2

    return OnEventsName


@click.command("go", help="Generate action github actions for go", epilog=ACTION_DOC_LONG)
@click.option("-n", "--name", nargs=1, help="Name of the action", prompt="Name of the action", required=True)
@click.option("-b", "--branch_name", help="Branch to add", prompt="Name of the branch", required=True)
@click.option("-a", "--action", help="Action to add", prompt="Action to add", required=True)
@click.option("-v", "--version", nargs=1, help="Version of go [default=1.17]", type=click.STRING, default="1.17",
              required=False)
def action_go(name, branch_name, action, version):
    version = version.split(",")
    if len(version) == 1:
        version = [version[0]]

    if len(branch_name.split(" ")) == 1:
        click.echo("Branch required 2 parameters! Example: push main,master")
        return

    on_event = OnEventFactory.create_events(on_events(branch_name.split(",")))
    action_ciGen_golang = ActionCIGenGolang()
    action_ciGen_golang.builder = GoActionBuilderImpl(name, version, on_event)

    ciGen = action_params_valid(action_ciGen_golang, action)

    confirm = click.confirm("Do you want to generate the action?")
    if confirm:
        print("Generating action...")
        nameFile = name.replace(" ", "_")
        pathFile = ".github/workflows/{}.yml".format(nameFile.lower())
        generate_action(path=pathFile, content=ciGen)
    else:
        click.echo("Aborted!")


def action_builder(action_ciGen_golang, actions):
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

    if isinstance(actions, int):
        matching_action = next((key for key, value in action_mapping.items() if value["action_id"] == actions),
                               None)
        if matching_action:
            action_data = action_mapping[matching_action]
            for step in action_data["steps"]:
                step()
        else:
            print("Action ID not found")
    elif actions in action_mapping:
        action_data = action_mapping[actions]
        for step in action_data["steps"]:
            step()
    else:
        print("Action not found")

    return action_ciGen_golang
