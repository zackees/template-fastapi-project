"""
Example test.
"""

import os
import unittest

from fastapi_template_project.version import VERSION

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
PYPROJECT_TOML = os.path.join(PROJECT_ROOT, "pyproject.toml")


class ExampleTester(unittest.TestCase):
    """Example tester."""

    def test_example(self) -> None:
        """Example tester."""
        with open(PYPROJECT_TOML, encoding="utf-8", mode="r") as pyproject_file:
            pyproject_lines = pyproject_file.read().splitlines()
        version = None
        for line in pyproject_lines:
            if line.startswith("version ="):
                version = line.split("=")[1].strip().strip('"')
                break
        self.assertEqual(version, VERSION, f"Version mismatch, {version} != {VERSION}")


if __name__ == "__main__":
    unittest.main()
