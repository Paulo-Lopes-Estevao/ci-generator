import unittest

from cigen.core.github.github_action import On, Push, PullRequest, Steps, OnEventFactory
from cigen.core.github.nodejs_action import NodejsActionSteps, NodejsAction, ActionCIGenNodejs, NodejsActionBuilderImpl


class NodejsTestCase(unittest.TestCase):

    def test_something(self):
        self.assertEqual(True, True)

    def test_base(self):
        on = On(
            Push(['main']),
            PullRequest(['main'])
        )
        node_action_steps = NodejsActionSteps('14.x')

        steps = Steps([
            node_action_steps.step_checkout(),
            node_action_steps.step_setup_node(),
            node_action_steps.step_install_dependencies(),
            node_action_steps.step_build(),
            node_action_steps.step_test(),
        ])

        node_action = NodejsAction(
            'Node Action',
            node_action_steps.version,
            on.to_dict(),
            steps,
            {
                'NODE_VERSION': '14.x'
            }
        )

        self.assertEqual(node_action.base(), {
            'name': 'Node Action',
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
                        node_action_steps.step_checkout(),
                        node_action_steps.step_setup_node(),
                        node_action_steps.step_install_dependencies(),
                        node_action_steps.step_build(),
                        node_action_steps.step_test(),
                    ]
                }
            }
        })

    def test_base_env(self):
        on = On(
            Push(['main']),
            PullRequest(['main'])
        )
        node_action_steps = NodejsActionSteps('14.x')

        steps = Steps([
            node_action_steps.step_checkout(),
            node_action_steps.step_setup_node(),
            node_action_steps.step_install_dependencies(),
            node_action_steps.step_build(),
            node_action_steps.step_test(),
        ])

        node_action = NodejsAction(
            'Node Action',
            node_action_steps.version,
            on.to_dict(),
            steps,
            {
                'NODE_VERSION': '14.x'
            }
        )

        self.assertEqual(node_action.run_with_env(), {
            'name': 'Node Action',
            'on': {
                'push': {
                    'branches': ['main']
                },
                'pull_request': {
                    'branches': ['main']
                }
            },
            'env': {
                'NODE_VERSION': '14.x'
            },
            'jobs': {
                'build': {
                    'name': 'Build',
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        node_action_steps.step_checkout(),
                        node_action_steps.step_setup_node(),
                        node_action_steps.step_install_dependencies(),
                        node_action_steps.step_build(),
                        node_action_steps.step_test(),
                    ]
                }
            }
        })

    def test_base_version_list(self):
        on = On(
            Push(['main']),
            PullRequest(['main'])
        )
        node_action_steps = NodejsActionSteps(['14.x', '15.x'])

        steps = Steps([
            node_action_steps.step_checkout(),
            node_action_steps.step_setup_node(),
            node_action_steps.step_install_dependencies(),
            node_action_steps.step_build(),
            node_action_steps.step_test(),
        ])

        node_action = NodejsAction(
            'Node Action',
            node_action_steps.version,
            on.to_dict(),
            steps,
        )

        self.assertEqual(node_action.base_version_list(), {
            'name': 'Node Action',
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
                    'strategy': {
                        'matrix': {
                            'node-version': ['14.x', '15.x']
                        },
                    },
                    'steps': [
                        node_action_steps.step_checkout(),
                        node_action_steps.step_setup_node(),
                        node_action_steps.step_install_dependencies(),
                        node_action_steps.step_build(),
                        node_action_steps.step_test(),
                    ]
                }
            }
        })

    def test_action_ci_base(self):
        action_ciGen_node = ActionCIGenNodejs()

        on_event_push = OnEventFactory.create_push(['main', 'master']).to_dict()

        action_ciGen_node.builder = NodejsActionBuilderImpl('Node Action', '14.x', on_event_push)

        action_ciGen_node.builder.step_checkout()
        action_ciGen_node.builder.step_setup_node()
        action_ciGen_node.builder.step_install_dependencies()
        action_ciGen_node.builder.step_build()
        action_ciGen_node.builder.step_test()

        self.assertEqual(action_ciGen_node.action_build_base(), {
            'name': 'Node Action',
            'on': {
                'push': {
                    'branches': ['main', 'master']
                },
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
                            'name': 'Setup Node',
                            'uses': 'actions/setup-node@v4',
                            'with': {
                                'node-version': '14.x'
                            }
                        },
                        {
                            'name': 'Install Dependencies',
                            'run': 'npm ci'
                        },
                        {
                            'name': 'Build',
                            'run': 'npm run build --if-present'
                        },
                        {
                            'name': 'Test',
                            'run': 'npm run test'
                        }
                    ]
                }
            }
        })

    def test_action_ci_base_default_build(self):
        action_ciGen_node = ActionCIGenNodejs()

        on_event_push = OnEventFactory.create_push(['main', 'master']).to_dict()

        action_ciGen_node.builder = NodejsActionBuilderImpl('Node Action', '14.x', on_event_push)

        action_ciGen_node.build_base()

        self.assertEqual(action_ciGen_node.action_build_base(), {
            'name': 'Node Action',
            'on': {
                'push': {
                    'branches': ['main', 'master']
                },
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
                            'name': 'Setup Node',
                            'uses': 'actions/setup-node@v4',
                            'with': {
                                'node-version': '14.x'
                            }
                        },
                        {
                            'name': 'Install Dependencies',
                            'run': 'npm ci'
                        },
                        {
                            'name': 'Build',
                            'run': 'npm run build --if-present'
                        },
                        {
                            'name': 'Test',
                            'run': 'npm run test'
                        }
                    ]
                }
            }
        })

    def test_action_ci_base_default_build_list(self):
        action_ciGen_node = ActionCIGenNodejs()

        on_event_push = OnEventFactory.create_push(['main', 'master']).to_dict()

        action_ciGen_node.builder = NodejsActionBuilderImpl('Node Action', ['14.x', '15.x'], on_event_push)

        action_ciGen_node.build_base_with_version_list()

        self.assertEqual(action_ciGen_node.action_build_base_version_list(), {
            'name': 'Node Action',
            'on': {
                'push': {
                    'branches': ['main', 'master']
                },
            },
            'jobs': {
                'build': {
                    'name': 'Build',
                    'runs-on': 'ubuntu-latest',
                    'strategy': {
                        'matrix': {
                            'node-version': ['14.x', '15.x']
                        },
                    },
                    'steps': [
                        {
                            'name': 'Checkout',
                            'uses': 'actions/checkout@v4'
                        },
                        {
                            'name': 'Setup Node',
                            'uses': 'actions/setup-node@v4',
                            'with': {
                                'node-version': '${{ matrix.node-version }}'
                            }
                        },
                        {
                            'name': 'Install Dependencies',
                            'run': 'npm ci'
                        },
                        {
                            'name': 'Build',
                            'run': 'npm run build --if-present'
                        },
                        {
                            'name': 'Test',
                            'run': 'npm run test'
                        }
                    ]
                }
            }
        })