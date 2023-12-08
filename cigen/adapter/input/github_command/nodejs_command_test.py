import unittest

from cigen.adapter.input.github_command.nodejs_command import action_nodejs
from click.testing import CliRunner


class NodeJSCommandTest(unittest.TestCase):
    runner = CliRunner()

    def test_something(self):
        self.assertEqual(True, True)

    def test_nodejs_command(self):
        result = self.runner.invoke(action_nodejs, ["-n", "Test NodeJS Action", "-b", "push main", "-a", "1"],
                                    input="y")

        self.assertEqual(result.exit_code, 0)
        self.assertIn("'name': 'Test NodeJS Action'", result.output)
