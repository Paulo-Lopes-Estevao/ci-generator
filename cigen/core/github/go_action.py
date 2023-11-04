import yaml
from cigen.core.github.github_action import On, Steps


class GoAction:
    on: On
    steps: Steps

    def __init__(self, name, version, on, steps: Steps, env=None) -> None:
        self.name = name
        self.version = version
        self.on = on
        self.steps = steps
        self.env = env

    def base(self):
        return {
            'name': self.name,
            'on': self.on,
            'jobs': {
                'build': {
                    'name': 'Build',
                    'runs-on': 'ubuntu-latest',
                    'steps': self.steps.to_dict()
                }
            }
        }

    def base_version_list(self):
        return {
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

    def base_to_yaml(self):
        return yaml.dump(self.base())

    def run(self):
        return self.base()

    def runWithEnv(self):
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
    def stepCheckout():
        return {
            'name': 'Checkout',
            'uses': 'actions/checkout@v4'
        }

    def stepSetupGo(self):
        if self.version is list:
            raise Exception('Version size must be 1 using Version range')

        return {
            'name': 'Setup Go',
            'uses': 'actions/setup-go@v4',
            'with': {
                'go-version': self.version
            }
        }

    def stepSetupGoWithVersionList(self):
        return {
            'strategy': {
                'matrix': {
                    'go-version': self.version if self.version is None else self.VersionListDefault()
                }
            },
            'steps': [
                self.stepCheckout(),
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
    def stepRunCache():
        return {
            'name': 'Cache',
            'uses': 'actions/cache@v2',
            'with': {
                'path': '~/.cache/go-build',
                'key': '${{ runner.os }}-go-${{ hashFiles(\'**/go.sum\') }}'
            }
        }

    @staticmethod
    def stepRunInstallDependencies():
        return {
            'name': 'Install Dependencies',
            'run': 'go mod download'
        }

    @staticmethod
    def stepRunTests():
        return {
            'name': 'Run Tests',
            'run': 'go test ./...'
        }

    @staticmethod
    def stepRunTestsAndCoverage():
        return {
            'name': 'Run Tests and Coverage',
            'run': 'go test ./... -coverprofile=coverage.out'
        }

    @staticmethod
    def stepRunTestsAndCoverageWithCoverage():
        return {
            'name': 'Run Tests and Coverage',
            'run': 'go test ./... -coverprofile=coverage.out && go tool cover -func=coverage.out'
        }

    @staticmethod
    def stepRunTestsAndCoverageWithCoverageAndHtml():
        return {
            'name': 'Run Tests and Coverage',
            'run': 'go test ./... -coverprofile=coverage.out && go tool cover -html=coverage.out'
        }

    @staticmethod
    def stepRunTestsAndCoverageWithCoverageAndHtmlAndUpload():
        return {
            'name': 'Run Tests and Coverage',
            'run': 'go test ./... -coverprofile=coverage.out && go tool cover -html=coverage.out && bash <(curl -s https://codecov.io/bash)'
        }

    @staticmethod
    def stepRunBuild():
        return {
            'name': 'Build',
            'run': 'go build ./...'
        }

    @staticmethod
    def VersionListDefault():
        return ['1.19', '1.20', '1.21.x']
