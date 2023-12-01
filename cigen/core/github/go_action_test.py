import unittest

from cigen.core.github.go_action import GoAction, GoActionSteps, ActionCIGenGolang, GoActionBuilderImpl
from cigen.core.github.github_action import On, Steps, Push, PullRequest, OnEventFactory


class GoActionTestCase(unittest.TestCase):
    def test_something(self):
        self.assertNotEqual(True, False)  # add assertion here

    def test_base(self):
        on = On(
            Push(['main']),
            PullRequest(['main'])
        )
        go_action_steps = GoActionSteps('1.17')

        steps = Steps([
            go_action_steps.step_checkout(),
            go_action_steps.step_setup_go(),
            go_action_steps.step_run_build(),
            go_action_steps.step_run_tests(),
        ])

        go_action = GoAction(
            'Go Action',
            go_action_steps.version,
            on.to_dict(),
            steps,
            {
                'GO_VERSION': '1.17'
            }
        )

        self.assertEqual(go_action.base(), {
            'name': 'Go Actions',
            'on': {
                'push': {
                    'branches': ['main']
                },
                'pull_request': {
                    'branches': ['main']
                }
            },
            'jobs': {
                'build': {
                    'name': 'Build',
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        go_action_steps.step_checkout(),
                        go_action_steps.step_setup_go(),
                        go_action_steps.step_run_build(),
                        go_action_steps.step_run_tests(),
                    ]
                }
            }
        })

    def test_base_push(self):
        on = On(
            Push(['main']),
            PullRequest(['main'])
        )
        go_action_steps = GoActionSteps(['1.17'])

        steps = Steps([
            go_action_steps.step_checkout(),
            go_action_steps.step_setup_go(),
            go_action_steps.step_run_build(),
            go_action_steps.step_run_tests(),
        ])

        go_action = GoAction(
            'Go Action',
            go_action_steps.version,
            on.on_push(),
            steps,
            {
                'GO_VERSION': '1.17'
            }
        )

        self.assertEqual(go_action.base(), {
            'name': 'Go Action',
            'on': {
                'push': {
                    'branches': ['main']
                }
            },
            'jobs': {
                'build': {
                    'name': 'Build',
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        go_action_steps.step_checkout(),
                        go_action_steps.step_setup_go(),
                        go_action_steps.step_run_build(),
                        go_action_steps.step_run_tests(),
                    ]
                }
            }
        })

    def test_go_runVersionWithRange(self):
        on = On(
            Push(['main']),
            PullRequest(['main'])
        )
        go_action_steps = GoActionSteps(['1.19'])

        steps = Steps([
            go_action_steps.step_setup_go_with_version_list()['steps'],
            go_action_steps.step_run_build(),
            go_action_steps.step_run_tests(),
        ])

        go_action = GoAction(
            'Go Action',
            go_action_steps.version,
            on.on_push(),
            steps,
        )

        print(go_action.base_version_list())

        self.assertEqual(go_action.base_version_list(), {
            'name': 'Go Action',
            'on': {
                'push': {
                    'branches': ['main']
                }
            },
            'jobs': {
                'build': {
                    'name': 'Build',
                    'runs-on': 'ubuntu-latest',
                    'strategy': {
                        'matrix': {
                            'go-version': go_action_steps.version
                        }
                    },
                    'steps': [
                        go_action_steps.step_setup_go_with_version_list()['steps'],
                        go_action_steps.step_run_build(),
                        go_action_steps.step_run_tests(),
                    ]
                }
            }
        })

    def test_action_ci_base(self):
        action_ciGen_golang = ActionCIGenGolang()

        on_event_push = OnEventFactory.create_push(['main', 'master']).to_dict()

        action_ciGen_golang.builder = GoActionBuilderImpl('Go Action', '1.17', on_event_push)
        action_ciGen_golang.builder.set_version('1.17')
        action_ciGen_golang.builder.step_checkout()
        action_ciGen_golang.builder.step_setup_go()
        action_ciGen_golang.builder.step_run_build()

        self.assertEqual(action_ciGen_golang.action_build_base(), {
            'name': 'Go Action',
            'on': {
                'push': {
                    'branches': ['main', 'master']
                }
            },
            'jobs': {
                'build': {
                    'name': 'Build',
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {
                            'name': 'Checkout',
                            'uses': 'actions/checkout@v4'
                        },
                        {
                            'name': 'Setup Go',
                            'uses': 'actions/setup-go@v4',
                            'with': {
                                'go-version': '1.17'
                            }
                        },
                        {
                            'name': 'Build',
                            'run': 'go build ./...'
                        }
                    ]
                }
            }
        })

    def test_action_ci_base_push_and_pull_request(self):
        action_ciGen_golang = ActionCIGenGolang()

        on_events = OnEventFactory.create_events({
            'push': {
                'branches': ['main', 'master']
            },
            'pull_request': {
                'branches': ['main', 'master']
            }
        })

        action_ciGen_golang.builder = GoActionBuilderImpl('Go Action', '1.17', on_events)
        action_ciGen_golang.builder.set_version('1.17')
        action_ciGen_golang.builder.step_checkout()
        action_ciGen_golang.builder.step_setup_go()
        action_ciGen_golang.builder.step_run_build()

        self.assertEqual(action_ciGen_golang.action_build_base(), {
            'name': 'Go Action',
            'on': {
                'push': {
                    'branches': ['main', 'master']
                },
                'pull_request': {
                    'branches': ['main', 'master']
                }
            },
            'jobs': {
                'build': {
                    'name': 'Build',
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {
                            'name': 'Checkout',
                            'uses': 'actions/checkout@v4'
                        },
                        {
                            'name': 'Setup Go',
                            'uses': 'actions/setup-go@v4',
                            'with': {
                                'go-version': '1.17'
                            }
                        },
                        {
                            'name': 'Build',
                            'run': 'go build ./...'
                        }
                    ]
                }
            }
        })

    def test_action_ci_build_base_with_version_list_push_and_pull_request(self):
        action_ciGen_golang = ActionCIGenGolang()

        on_events = OnEventFactory.create_events({
            'push': {
                'branches': ['main', 'master']
            },
            'pull_request': {
                'branches': ['main', 'master']
            }
        })

        action_ciGen_golang.builder = GoActionBuilderImpl('Go Action', ['1.17', '1.18', '1.19'], on_events)
        action_ciGen_golang.builder.step_checkout()
        action_ciGen_golang.builder.step_setup_go_with_versions_matrix()
        action_ciGen_golang.builder.step_run_build()

        self.assertEqual(action_ciGen_golang.action_build_base_with_version_list(), {
            'name': 'Go Action',
            'on': {
                'push': {
                    'branches': ['main', 'master']
                },
                'pull_request': {
                    'branches': ['main', 'master']
                }
            },
            'jobs': {
                'build': {
                    'name': 'Build',
                    'runs-on': 'ubuntu-latest',
                    'strategy': {
                        'matrix': {
                            'go-version': ['1.17', '1.18', '1.19']
                        }
                    },
                    'steps': [
                        {
                            'name': 'Checkout',
                            'uses': 'actions/checkout@v4'
                        },
                        {
                            'name': 'Setup Go',
                            'uses': 'actions/setup-go@v4',
                            'with': {
                                'go-version': '${{ matrix.go-version }}'
                            }
                        },
                        {
                            'name': 'Build',
                            'run': 'go build ./...'
                        }
                    ]
                }
            }
        })


if __name__ == '__main__':
    unittest.main()
