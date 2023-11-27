import pprint

import click

from cigen.core.github.github_action import OnEventFactory
from cigen.core.github.go_action import GoActionBuilderImpl, ActionCIGenGolang


class AddCommand:
    def __init__(self):
        pass

    @staticmethod
    def list_steps():
        return [
            "build_base",
            "build_base_with_version_list",
            "checkout",
            "setup_go",
            "setup_go_with_version_list",
            "build",
            "cache",
            "install_dependencies",
            "tests",
            "tests_and_coverage",
            "tests_and_coverage_with_coverage",
            "tests_and_coverage_with_coverage_and_html",
            "tests_and_coverage_with_coverage_and_html_and_upload",
        ]

    @staticmethod
    def on_events(listEvent: list[str]) -> dict:
        branchs = {}
        brancheName = {}
        if len(listEvent) == 2:
            brancheName['branches'] = listEvent[1].split(",")
            branchs[listEvent[0]] = brancheName
            return branchs

        countElements = 0
        for i in range(len(listEvent)):
            if countElements >= len(listEvent):
                break

            brancheName['branches'] = listEvent[countElements + 1].split(",")
            branchs[listEvent[countElements]] = brancheName
            countElements += 2

        return branchs

    @click.command()
    @click.option("--step", "-s", nargs=-1, type=click.Choice(list_steps()), help="Steps list", required=False)
    def steps(self, steps):
        click.echo(pprint.pprint(self.list_steps()))

    @click.command()
    @click.option("-n", "--name", nargs=1, help="Name of the action", prompt="Name of the action", required=True)
    @click.option("-b", "--branch_name", nargs=-1, help="Branch to add", prompt="Name of the branch", required=True)
    @click.option("-a", "--action", nargs=-1, help="Action to add", default="go", required=True)
    @click.option("-v", "--version", nargs=1, help="Version of go", type=click.STRING, default="1.17", required=False)
    def action(self, name, branch_name, action, version):
        """

        :param name:
        :param branch_name:
        :param action:
        :param version:
        :return:

        Actions:
        0 - base
        1 - version_list
        2 - build_base
        3 - build_base_with_version_list
        4 - checkout
        5 - setup_go
        6 - setup_go_with_version_list
        7 - build
        8 - cache
        9 - install_dependencies
        10 - tests
        11 - tests_and_coverage
        12 - tests_and_coverage_with_coverage
        13 - tests_and_coverage_with_coverage_and_html
        14 - tests_and_coverage_with_coverage_and_html_and_upload

        base ou version_list 0 ou 1 is required like last parameter

        :example: 2,3,5 0


        """

        on_events = OnEventFactory.create_events(self.on_events(branch_name))
        action_ciGen_golang = ActionCIGenGolang()
        action_ciGen_golang.builder = GoActionBuilderImpl(name, version, on_events)
        for actions in action:
            self.action_builder(action_ciGen_golang, actions)

    @staticmethod
    def action_builder(action_ciGen_golang, actions):
        if actions == "base" or actions == 0:
            action_ciGen_golang.action_build_base()
        elif actions == "version_list" or actions == 1:
            action_ciGen_golang.action_build_base_with_version_list()
        if actions == "build_base" or actions == 2:
            action_ciGen_golang.builder.step_checkout()
            action_ciGen_golang.builder.step_setup_go()
            action_ciGen_golang.builder.step_run_build()
            action_ciGen_golang.builder.step_run_tests()
            action_ciGen_golang.action_build_base()
        elif actions == "build_base_with_version_list" or actions == 3:
            action_ciGen_golang.builder.step_checkout()
            action_ciGen_golang.builder.step_setup_go()
            action_ciGen_golang.builder.step_run_build()
            action_ciGen_golang.builder.step_run_tests()
            action_ciGen_golang.action_build_base_with_version_list()
        elif actions == "checkout" or actions == 4:
            action_ciGen_golang.builder.step_checkout()
        elif actions == "setup_go" or actions == 5:
            action_ciGen_golang.builder.step_setup_go()
        elif actions == "setup_go_with_version_list" or actions == 6:
            action_ciGen_golang.builder.step_setup_go_with_version_list()
        elif actions == "build" or actions == 7:
            action_ciGen_golang.builder.step_run_build()
        elif actions == "cache" or actions == 8:
            action_ciGen_golang.builder.step_run_cache()
        elif actions == "install_dependencies" or actions == 9:
            action_ciGen_golang.builder.step_run_install_dependencies()
        elif actions == "tests" or actions == 10:
            action_ciGen_golang.builder.step_run_tests()
        elif actions == "tests_and_coverage" or actions == 11:
            action_ciGen_golang.builder.step_run_tests_and_coverage()
        elif actions == "tests_and_coverage_with_coverage" or actions == 12:
            action_ciGen_golang.builder.step_run_tests_and_coverage_with_coverage()
        elif actions == "tests_and_coverage_with_coverage_and_html" or actions == 13:
            action_ciGen_golang.builder.step_run_tests_and_coverage_with_coverage_and_html()
        elif actions == "tests_and_coverage_with_coverage_and_html_and_upload" or actions == 14:
            action_ciGen_golang.builder.step_run_tests_and_coverage_with_coverage_and_html_and_upload()
        else:
            click.echo("Action not found")
            return
