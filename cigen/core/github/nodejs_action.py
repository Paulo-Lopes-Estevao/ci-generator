from __future__ import annotations

from abc import ABC, abstractmethod

from cigen.core.github.github_action import Steps, Action


class NodejsActionBuilder(ABC):

    @property
    @abstractmethod
    def build(self) -> Action:
        pass

    @property
    @abstractmethod
    def build_steps(self) -> NodejsActionSteps:
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
    def step_setup_node(self) -> None:
        pass

    @abstractmethod
    def step_setup_node_with_version_matrix(self) -> None:
        pass

    @abstractmethod
    def step_install_dependencies(self) -> None:
        pass

    @abstractmethod
    def step_build(self) -> None:
        pass

    @abstractmethod
    def step_test(self) -> None:
        pass

    @abstractmethod
    def step_publish(self) -> None:
        pass

    @abstractmethod
    def step_publish_with_tag(self) -> None:
        pass

    @abstractmethod
    def step_publish_with_access(self) -> None:
        pass

    @abstractmethod
    def step_security_scan(self) -> None:
        pass

    @abstractmethod
    def step_run_cache(self) -> None:
        pass


class NodejsActionBuilderImpl(NodejsActionBuilder):

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
        self._build = Action(self.name, self.version, self.on, self.step, self.env)

    def reset_steps(self):
        self._steps = NodejsActionSteps(self.version)

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

    def step_setup_node(self):
        self.step.add_at(self._steps.step_setup_node(), 1)

    def step_setup_go_with_version_list(self):
        self.step.add(self._steps.step_setup_go_with_version_list())

    def step_install_dependencies(self):
        self.step.add(self._steps.step_install_dependencies())

    def step_publish(self):
        self.step.add(self._steps.step_publish())

    def step_publish_with_tag(self):
        self.step.add(self._steps.step_publish_with_tag())

    def step_publish_with_access(self):
        self.step.add(self._steps.step_publish_with_access())

    def step_security_scan(self):
        self.step.add(self._steps.step_security_scan())

    def step_setup_node_with_version_matrix(self):
        self.step.add_at(self._steps.step_setup_node_with_version_matrix(), 1)

    def step_run_cache(self):
        self.step.add(self._steps.step_run_cache())

    def step_run_install_dependencies(self):
        self.step.add(self._steps.step_run_install_dependencies())

    def step_test(self):
        self.step.add(self._steps.step_test())

    def step_run_tests_and_coverage(self):
        self.step.add(self._steps.step_run_tests_and_coverage())

    def step_run_tests_and_coverage_with_coverage(self):
        self.step.add(self._steps.step_run_tests_and_coverage_with_coverage())

    def step_run_tests_and_coverage_with_coverage_and_html(self):
        self.step.add(self._steps.step_run_tests_and_coverage_with_coverage_and_html())

    def step_run_tests_and_coverage_with_coverage_and_html_and_upload(self):
        self.step.add(self._steps.step_run_tests_and_coverage_with_coverage_and_html_and_upload())

    def step_build(self):
        self.step.add(self._steps.step_build())

    def version_list_default(self):
        self._steps.version_list_default()

    def set_version(self, param):
        self._steps.version = param


class NodejsActionSteps:

    def __init__(self, version) -> None:
        if version is None:
            raise TypeError("Version is required")
        self.version = version

    @staticmethod
    def step_checkout():
        return {
            'name': 'Checkout',
            'uses': 'actions/checkout@v4'
        }

    def step_setup_node(self):
        if self.version is list:
            raise Exception('Version size must be 1 using Version range')

        return {
            'name': 'Setup Node',
            'uses': 'actions/setup-node@v4',
            'with': {
                'node-version': self.version
            }
        }

    @staticmethod
    def step_setup_node_with_version_matrix():
        return {
            'name': 'Setup Node',
            'uses': 'actions/setup-node@v4',
            'with': {
                'node-version': '${{ matrix.node-version }}'
            }
        }

    @staticmethod
    def step_run_cache():
        return {
            'name': 'Cache',
            'uses': 'actions/cache@v2',
            'with': {
                'path': 'node_modules',
                'key': '${{ runner.os }}-node-${{ hashFiles(\'**/package-lock.json\') }}',
                'restore-keys': '${{ runner.os }}-node-'
            }
        }

    @staticmethod
    def step_install_dependencies():
        return {
            'name': 'Install Dependencies',
            'run': 'npm ci'
        }

    @staticmethod
    def step_build():
        return {
            'name': 'Build',
            'run': 'npm run build --if-present'
        }

    @staticmethod
    def step_test():
        return {
            'name': 'Test',
            'run': 'npm run test'
        }

    @staticmethod
    def step_publish():
        return {
            'name': 'Publish',
            'run': 'npm publish'
        }

    @staticmethod
    def step_publish_with_tag():
        return {
            'name': 'Publish',
            'run': 'npm publish --tag ${{ github.ref_name }}'
        }

    @staticmethod
    def step_publish_with_access():
        return {
            'name': 'Publish',
            'run': 'npm publish --access public'
        }

    @staticmethod
    def step_security_scan():
        return {
            'runs-on': 'ubuntu-latest',
            'name': 'Security Scan',
            'steps': [
                {
                    'name': 'Checkout',
                    'uses': 'actions/checkout@v4'
                },
                {
                    'name': 'nodejs-security-scan',
                    'id': 'nodejs-security-scan',
                    'uses': 'ajinabraham/njsscan-action@master',
                    'with': {
                        'args': '.'
                    }
                }
            ]
        }


class ActionCIGenNodejs:

    def __init__(self):
        self._builder = None

    @property
    def builder(self) -> NodejsActionBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: NodejsActionBuilder) -> None:
        self._builder = builder

    def action_build_base(self):
        return self.builder.base()

    def action_build_base_version_list(self):
        return self.builder.base_version_list()

    def action_build_base_to_yaml(self):
        return self.builder.base_to_yaml()

    def action_build_run(self):
        return self.builder.run()

    def action_build_run_with_env(self):
        return self.builder.run_with_env()

    def action_build_steps(self):
        return self.builder.add_steps(self.builder.build_steps)

    def build_base(self):
        self.builder.step_checkout()
        self.builder.step_setup_node()
        self.builder.step_install_dependencies()
        self.builder.step_build()
        self.builder.step_test()
        return self.builder.build

    def build_base_with_version_list(self):
        self.builder.step_checkout()
        self.builder.step_setup_node_with_version_matrix()
        self.builder.step_install_dependencies()
        self.builder.step_build()
        self.builder.step_test()
        return self.builder.build
