import unittest

from cigen.adapter.input.github_command.go_command import action_go
from click.testing import CliRunner


class GoCommandTestCase(unittest.TestCase):
    runner = CliRunner()

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_action_build_base(self):
        result = self.runner.invoke(action_go, ["-n", "Test Go Action", "-b", "push main", "-a", "1"], input="y")

        self.assertEqual(result.exit_code, 0)
        self.assertIn("'name': 'Test Go Action'", result.output)


if __name__ == '__main__':
    unittest.main()
