import unittest
from cigen.core.github.github_action import On, Steps, Push, PullRequest


class GithubActionTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_on(self):
        on = On(
            Push(['main']),
            PullRequest(['main'])
        )
        self.assertEqual(on.to_dict(), {
            'push': {
                'branches': ['main']
            },
            'pull_request': {
                'branches': ['main']
            }
        })

    def test_on_push(self):
        on = On(
            Push(['main']),
            PullRequest(['main'])
        )
        self.assertEqual(on.onPush(), {
            'push': {
                'branches': ['main']
            }
        })

    def test_on_pull_request(self):
        on = On(
            Push(['main']),
            PullRequest(['main'])
        )
        self.assertEqual(on.onPullRequest(), {
            'pull_request': {
                'branches': ['main']
            }
        })

    def test_on_yaml(self):
        on = On(
            Push(['main']),
            PullRequest(['main'])
        )
        self.assertEqual(on.to_yaml(), 'pull_request:\n  branches:\n  - main\npush:\n  branches:\n  - main\n')

    def test_steps(self):
        steps = Steps([
            {
                'name': 'Checkout',
                'uses': 'actions/checkout@v2'
            },
            {
                'name': 'Setup Go',
                'uses': 'actions/setup-go@v2',
                'with': {
                    'go-version': '1.16'
                }
            },
            {
                'name': 'Run Test',
                'run': 'go test ./...'
            }
        ])
        self.assertEqual(steps.to_dict(), [
            {
                'name': 'Checkout',
                'uses': 'actions/checkout@v2'
            },
            {
                'name': 'Setup Go',
                'uses': 'actions/setup-go@v2',
                'with': {
                    'go-version': '1.16'
                }
            },
            {
                'name': 'Run Test',
                'run': 'go test ./...'
            }
        ])

    def test_steps_two(self):
        step_one = {
            'name': 'Checkout',
            'uses': 'actions/checkout@v2'
        }
        step_two = {
            'name': 'Setup Go',
            'uses': 'actions/setup-go@v2',
            'with': {
                'go-version': '1.16'
            }
        }
        step_three = {
            'name': 'Run Test',
            'run': 'go test ./...'
        }

        steps = Steps([
            step_one,
            step_two,
            step_three
        ])

        self.assertEqual(steps.to_dict(), [
            step_one,
            step_two,
            step_three
        ])

    def test_steps_add_index(self):
        step_one = {
            'name': 'Checkout',
            'uses': 'actions/checkout@v2'
        }
        step_two = {
            'name': 'Setup Go',
            'uses': 'actions/setup-go@v2',
            'with': {
                'go-version': '1.16'
            }
        }
        step_three = {
            'name': 'Run Test',
            'run': 'go test ./...'
        }

        steps = Steps([
            step_one,
            step_two,
            step_three
        ])

        step_four = {
            'name': 'Run Test',
            'run': 'go test ./...'
        }

        steps.addAt(step_four, 1)

        self.assertEqual(steps.to_dict(), [
            step_one,
            step_four,
            step_two,
            step_three
        ])

    def test_steps_to_yml(self):
        steps = Steps([
            {
                'name': 'Checkout',
                'uses': 'actions/checkout@v2'
            },
            {
                'name': 'Setup Go',
                'uses': 'actions/setup-go@v2',
                'with': {
                    'go-version': '1.16'
                }
            },
            {
                'name': 'Run Test',
                'run': 'go test ./...'
            }
        ])
        self.assertEqual(steps.to_yaml(), '- name: Checkout\n  uses: actions/checkout@v2\n- name: Setup Go\n  uses: actions/setup-go@v2\n  with:\n    go-version: \'1.16\'\n- name: Run Test\n  run: go test ./...\n')


if __name__ == '__main__':
    unittest.main()
