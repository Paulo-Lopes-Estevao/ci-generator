import unittest
from cigen.core.github.github_action import On, Steps, Push, PullRequest, OnEventFactory


def step_exec():
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
    return step_one, step_three, step_two, steps


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
        self.assertEqual(on.on_push(), {
            'push': {
                'branches': ['main']
            }
        })

    def test_on_pull_request(self):
        on = On(
            Push(['main']),
            PullRequest(['main'])
        )
        self.assertEqual(on.on_pull_request(), {
            'pull_request': {
                'branches': ['main']
            }
        })

    def test_on_push_and_pull_request(self):
        on = On(
            Push(['main']),
            PullRequest(['main'])
        )
        self.assertEqual(on.on_push_and_pull_request(), {
            'push': {
                'branches': ['main']
            },
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
        step_one, step_three, step_two, steps = step_exec()

        self.assertEqual(steps.to_dict(), [
            step_one,
            step_two,
            step_three
        ])

    def test_steps_add_index(self):
        step_one, step_three, step_two, steps = step_exec()

        step_four = {
            'name': 'Run Test',
            'run': 'go test ./...'
        }

        steps.add_at(step_four, 1)

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
        self.assertEqual(steps.to_yaml(),
                         '- name: Checkout\n  uses: actions/checkout@v2\n- name: Setup Go\n  uses: '
                         'actions/setup-go@v2\n  with:\n    go-version: \'1.16\'\n- name: Run Test\n  run: go test '
                         './...\n')

    def test_on_event_push_json(self):
        on_event = OnEventFactory.create_push(['main', 'master'])

        self.assertEqual(on_event.to_dict(), {
            'push': {
                'branches': ['main', 'master']
            }
        })

    def test_on_event_pull_request_json(self):
        on_event = OnEventFactory.create_pull_request(['main', 'master'])

        self.assertEqual(on_event.to_dict(), {
            'pull_request': {
                'branches': ['main', 'master']
            }
        })

    def test_on_event_push_yaml(self):
        on_event = OnEventFactory.create_push(['main', 'master'])

        self.assertEqual(on_event.to_yaml(), 'push:\n  branches:\n  - main\n  - master\n')

    def test_on_event_pull_request_yaml(self):
        on_event = OnEventFactory.create_pull_request(['main', 'master'])

        self.assertEqual(on_event.to_yaml(), 'pull_request:\n  branches:\n  - main\n  - master\n')

    def test_on_events_push_pull_request(self):
        on_event = OnEventFactory.create_events({
            'push': {
                'branches': ['main', 'master']
            },
            'pull_request': {
                'branches': ['main', 'master']
            }
        })

        self.assertEqual(on_event, {
            'push': {
                'branches': ['main', 'master']
            },
            'pull_request': {
                'branches': ['main', 'master']
            }
        })


if __name__ == '__main__':
    unittest.main()
