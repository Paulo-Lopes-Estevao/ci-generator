from __future__ import annotations

import inspect
import yaml
from cigen.core.github.github_action import Steps, OnEvent
from abc import ABC, abstractmethod


class GoActionBuilder(ABC):

    @property
    @abstractmethod
    def build(self) -> GoAction:
        pass

    @property
    @abstractmethod
    def build_steps(self) -> GoActionSteps:
        pass

    @abstractmethod
    def base(self) -> None:
        pass

    @abstractmethod
    def base_version_list(self) -> None:
        pass

    def add_steps(self, step):
        pass

    @abstractmethod
    def base_to_yaml(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def run_with_env(self) -> None:
        pass

    @abstractmethod
    def step_checkout(self) -> None:
        pass

    @abstractmethod
    def step_setup_go(self) -> None:
        pass

    @abstractmethod
    def step_setup_go_with_version_list(self) -> None:
        pass

    @abstractmethod
    def step_setup_go_with_versions_matrix(self) -> None:
        pass

    @abstractmethod
    def step_run_cache(self) -> None:
        pass

    @abstractmethod
    def step_run_install_dependencies(self) -> None:
        pass

    @abstractmethod
    def step_run_tests(self) -> None:
        pass

    @abstractmethod
    def step_run_tests_and_coverage(self) -> None:
        pass

    @abstractmethod
    def step_run_tests_and_coverage_with_coverage(self) -> None:
        pass

    @abstractmethod
    def step_run_tests_and_coverage_with_coverage_and_html(self) -> None:
        pass

    @abstractmethod
    def step_run_tests_and_coverage_with_coverage_and_html_and_upload(self) -> None:
        pass

    @abstractmethod
    def step_run_build(self) -> None:
        pass

    @abstractmethod
    def version_list_default(self) -> None:
        pass

    @abstractmethod
    def set_version(self, param):
        pass

    def list_steps(self):
        pass


class GoActionBuilderImpl(GoActionBuilder):
    def __init__(self, name, version, on, env=None) -> None:
        self._steps = None
        self._build = None
        self.name = name
        self.version = version
        self.on = on
        self.env = env
        self.step = Steps([])
        self.reset()
        self.reset_steps()

    def reset(self):
        self._build = GoAction(self.name, self.version, self.on, self.step, self.env)

    def reset_steps(self):
        self._steps = GoActionSteps(self.version)

    @property
    def build_steps(self):
        build_steps = self._steps
        self.reset_steps()
        return build_steps

    def add_steps(self, step):
        return self.step.add(step)

    @property
    def build(self):
        build = self._build
        self.reset()
        return build

    def base(self):
        return self._build.base()

    def base_version_list(self):
        return self._build.base_version_list()

    def base_to_yaml(self):
        return self._build.base_to_yaml()

    def run(self):
        return self._build.run()

    def run_with_env(self):
        self.step.add(self._build.run_with_env())

    def step_checkout(self):
        self.step.add_at(self._steps.step_checkout(), 0)

    def step_setup_go(self):
        self.step.add_at(self._steps.step_setup_go(), 1)

    def step_setup_go_with_version_list(self):
        self.step.add(self._steps.step_setup_go_with_version_list())

    def step_setup_go_with_versions_matrix(self):
        self.step.add_at(self._steps.step_setup_go_with_versions_matrix(), 1)

    def step_run_cache(self):
        self.step.add(self._steps.step_run_cache())

    def step_run_install_dependencies(self):
        self.step.add(self._steps.step_run_install_dependencies())

    def step_run_tests(self):
        self.step.add(self._steps.step_run_tests())

    def step_run_tests_and_coverage(self):
        self.step.add(self._steps.step_run_tests_and_coverage())

    def step_run_tests_and_coverage_with_coverage(self):
        self.step.add(self._steps.step_run_tests_and_coverage_with_coverage())

    def step_run_tests_and_coverage_with_coverage_and_html(self):
        self.step.add(self._steps.step_run_tests_and_coverage_with_coverage_and_html())

    def step_run_tests_and_coverage_with_coverage_and_html_and_upload(self):
        self.step.add(self._steps.step_run_tests_and_coverage_with_coverage_and_html_and_upload())

    def step_run_build(self):
        self.step.add(self._steps.step_run_build())

    def version_list_default(self):
        self._steps.version_list_default()

    def set_version(self, param):
        self._steps.version = param


class GoAction:
    on: OnEvent
    steps: Steps

    def __init__(self, name, version, on, steps: Steps, env=None) -> None:
        self.name = name
        self.version = version
        self.on = on
        self.steps = steps
        self.env = env

    def base(self):
        print(self.on)

        action_base = {
            'name': self.name,
            "on": self.on,
            'jobs': {
                'build': {
                    'name': 'Build',
                    'runs-on': 'ubuntu-latest',
                    'steps': self.steps.to_dict()
                }
            }
        }
        return self.order_json(action_base, ['name', 'on', 'jobs'])

    def base_version_list(self):
        if self.version == [] or self.version == "" or self.version is None:
            self.version = ['1.19', '1.20', '1.21.x']

        action_base = {
            'name': self.name,
            'on': self.on,
            'jobs': {
                'build': {
                    'name': 'Build',
                    'runs-on': 'ubuntu-latest',
                    'strategy': {
                        'matrix': {
                            'go-version': self.version
                        },
                    },
                    'steps': self.steps.to_dict()
                }
            }
        }
        return self.order_json(action_base, ['name', 'on', 'jobs'])

    def order_json(self, json_obj, ordem):
        ordered_json = {key: json_obj[key] for key in ordem if key in json_obj}

        remaining_keys = [key for key in json_obj if key not in ordem]
        ordered_json.update({key: json_obj[key] for key in remaining_keys})

        for key, value in ordered_json.items():
            if isinstance(value, dict):
                ordered_json[key] = self.order_json(value, ordem)
            elif isinstance(value, list):
                ordered_json[key] = [self.order_json(item, ordem) if isinstance(item, dict) else item for item in value]

        return ordered_json

    def base_to_yaml(self):
        return yaml.dump(self.base())

    def run(self):
        return self.base()

    def run_with_env(self):
        return {
            **self.base(),
            'env': self.env
        }


class GoActionSteps:
    def __init__(self, version) -> None:
        if version is None:
            raise Exception('Version is required')
        self.version = version

    @staticmethod
    def step_checkout():
        return {
            'name': 'Checkout',
            'uses': 'actions/checkout@v4'
        }

    def step_setup_go(self):
        if self.version is list:
            raise Exception('Version size must be 1 using Version range')

        return {
            'name': 'Setup Go',
            'uses': 'actions/setup-go@v4',
            'with': {
                'go-version': self.version
            }
        }

    def step_setup_go_with_version_list(self):
        return {
            'strategy': {
                'matrix': {
                    'go-version': self.version if self.version is None else self.version_list_default()
                }
            },
            'steps': [
                self.step_checkout(),
                {
                    'name': 'Setup Go',
                    'uses': 'actions/setup-go@v4',
                    'with': {
                        'go-version': '${{ matrix.go-version }}'
                    }
                },
            ]
        }

    @staticmethod
    def step_setup_go_with_versions_matrix():
        return {
            'name': 'Setup Go',
            'uses': 'actions/setup-go@v4',
            'with': {
                'go-version': '${{ matrix.go-version }}'
            }
        }

    @staticmethod
    def step_run_cache():
        return {
            'name': 'Cache',
            'uses': 'actions/cache@v2',
            'with': {
                'path': '~/.cache/go-build',
                'key': '${{ runner.os }}-go-${{ hashFiles(\'**/go.sum\') }}'
            }
        }

    @staticmethod
    def step_run_install_dependencies():
        return {
            'name': 'Install Dependencies',
            'run': 'go mod download'
        }

    @staticmethod
    def step_run_tests():
        return {
            'name': 'Run Tests',
            'run': 'go test ./...'
        }

    @staticmethod
    def step_run_tests_and_coverage():
        return {
            'name': 'Run Tests and Coverage',
            'run': 'go test ./... -coverprofile=coverage.out'
        }

    @staticmethod
    def step_run_tests_and_coverage_with_coverage():
        return {
            'name': 'Run Tests and Coverage',
            'run': 'go test ./... -coverprofile=coverage.out && go tool cover -func=coverage.out'
        }

    @staticmethod
    def step_run_tests_and_coverage_with_coverage_and_html():
        return {
            'name': 'Run Tests and Coverage',
            'run': 'go test ./... -coverprofile=coverage.out && go tool cover -html=coverage.out'
        }

    @staticmethod
    def step_run_tests_and_coverage_with_coverage_and_html_and_upload():
        return {
            'name': 'Run Tests and Coverage',
            'run': 'go test ./... -coverprofile=coverage.out && go tool cover -html=coverage.out && bash <(curl -s '
                   'https://codecov.io/bash)'
        }

    @staticmethod
    def step_run_build():
        return {
            'name': 'Build',
            'run': 'go build ./...'
        }

    @staticmethod
    def version_list_default():
        return ['1.19', '1.20', '1.21.x']


class ActionCIGenGolang:

    def __init__(self):
        self._builder = None

    def __int__(self):
        self._builder = None

    @property
    def builder(self) -> GoActionBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: GoActionBuilder) -> None:
        self._builder = builder

    def action_build_base(self):
        return self.builder.base()

    def action_build_base_with_version_list(self):
        return self.builder.base_version_list()

    def _list_steps(self):
        return self.builder.list_steps()

    def _action_steps_run_build(self):
        self.builder.add_steps(self.builder.step_run_build())

