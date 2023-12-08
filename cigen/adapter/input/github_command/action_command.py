import pprint

import click

from cigen.adapter.output.github_out.file_action import generate_action


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


def version_format_param(version):
    version = version.split(",")
    if len(version) == 1:
        version = version[0]
    return version


def confirm_generation_action(ciGen, name):
    confirm = click.confirm("Do you want to generate the action?")
    if confirm:
        print("Generating action...")
        nameFile = name.replace(" ", "_")
        pathFile = ".github/workflows/{}.yml".format(nameFile.lower())
        generate_action(path=pathFile, content=ciGen)
    else:
        click.echo("Aborted!")


def action_format_param(action):
    lastElement = action.split(" ")[len(action.split(" ")) - 1]
    dropLastElement = action.split(" ")
    if len(dropLastElement) > 1:
        dropLastElement.pop()
        dropLastElement = dropLastElement[0].split(",")
    elements = dropLastElement
    return elements, lastElement


def action_validate_flag(action, elements):
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


def action_params_valid(elements, lastElement, action_ciGen, action):
    action_validate_flag(action, elements)

    if lastElement == "0" or elements[0] == "1":
        click.echo(pprint.pprint(action_ciGen.action_build_base()))
        return action_ciGen.action_build_base()
    elif lastElement == "1" or elements[0] == "2":
        click.echo(pprint.pprint(action_ciGen.action_build_base_with_version_list()))
        return action_ciGen.action_build_base_with_version_list()
    else:
        click.echo("Action not found")
        return


def on_branch_validate_param(branch_name):
    if len(branch_name.split(" ")) == 1:
        click.echo("Branch required 2 parameters! Example: push main,master")


def mapping_instance_action(action_mapping, actions):
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
        return
