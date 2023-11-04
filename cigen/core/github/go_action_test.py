import unittest
from cigen.core.github.go_action import GoAction, GoActionSteps
from cigen.core.github.github_action import On, Steps, Push, PullRequest



class GoActionTestCase(unittest.TestCase):
    def test_something(self):
        self.assertNotEquals(True, False)  # add assertion here

    def test_base(self):
        on = On(
            Push(['main']),
            PullRequest(['main'])
        )
        go_action_steps = GoActionSteps('1.17')

        steps = Steps([
            go_action_steps.stepCheckout(),
            go_action_steps.stepSetupGo(),
            go_action_steps.stepRunBuild(),
            go_action_steps.stepRunTests(),
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
            'name': 'Go Action',
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
                        go_action_steps.stepCheckout(),
                        go_action_steps.stepSetupGo(),
                        go_action_steps.stepRunBuild(),
                        go_action_steps.stepRunTests(),
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
            go_action_steps.stepCheckout(),
            go_action_steps.stepSetupGo(),
            go_action_steps.stepRunBuild(),
            go_action_steps.stepRunTests(),
            ])

        go_action = GoAction(
            'Go Action',
            go_action_steps.version,
            on.onPush(),
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
                        go_action_steps.stepCheckout(),
                        go_action_steps.stepSetupGo(),
                        go_action_steps.stepRunBuild(),
                        go_action_steps.stepRunTests(),
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
            go_action_steps.stepSetupGoWithVersionList()['steps'],
            go_action_steps.stepRunBuild(),
            go_action_steps.stepRunTests(),
            ])

        go_action = GoAction(
            'Go Action',
            go_action_steps.version,
            on.onPush(),
            steps,
        )

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
                        go_action_steps.stepSetupGoWithVersionList()['steps'],
                        go_action_steps.stepRunBuild(),
                        go_action_steps.stepRunTests(),
                    ]
                }
            }
        })






if __name__ == '__main__':
    unittest.main()
